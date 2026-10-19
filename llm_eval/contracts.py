"""Bounded JSON input, canonical fingerprints, and task contract validation."""

import hashlib
import json
import math
from importlib.resources import files
from pathlib import Path

MAX_FILE_BYTES = 20_000_000
MAX_RESPONSE_CHARS = 1_000_000
DECISIONS = {"accept", "review", "reject"}
FIELDS = {"supplier", "units", "unit_price_eur"}


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def parse_json(text):
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)


def read_json(path):
    path = Path(path)
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"Input exceeds {MAX_FILE_BYTES} bytes")
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"Input exceeds {MAX_FILE_BYTES} bytes")
    return parse_json(data.decode("utf-8"))


def fixture(name):
    return parse_json(files("llm_eval").joinpath("fixtures", name).read_text(encoding="utf-8"))


def fingerprint(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def number(value, label, minimum=0, maximum=None):
    try:
        finite = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError(f"{label} must be a finite number")
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{label} is outside the allowed range")


def integer(value, label, minimum=1, maximum=100):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be an integer from {minimum} to {maximum}")


def response_shape(value):
    """Return a shape error; exact field types keep bool != number."""
    if not isinstance(value, dict) or set(value) != {"decision", "fields", "evidence_ids", "reason"}:
        return "Expected exactly decision, fields, evidence_ids, reason"
    if not isinstance(value["decision"], str) or value["decision"] not in DECISIONS:
        return "Invalid decision"
    fields = value["fields"]
    if not isinstance(fields, dict) or set(fields) != FIELDS:
        return "Invalid fields object"
    if fields["supplier"] is not None and (not isinstance(fields["supplier"], str) or not fields["supplier"].strip()):
        return "supplier must be a nonempty string or null"
    if fields["units"] is not None:
        try:
            integer(fields["units"], "units", maximum=1_000_000)
        except ValueError as exc:
            return str(exc)
    if fields["unit_price_eur"] is not None:
        try:
            number(fields["unit_price_eur"], "unit_price_eur", maximum=1_000_000)
        except ValueError as exc:
            return str(exc)
    ids = value["evidence_ids"]
    if not isinstance(ids, list) or any(not isinstance(item, str) or not item for item in ids):
        return "evidence_ids must be a list of nonempty strings"
    if len(ids) != len(set(ids)):
        return "Duplicate evidence IDs"
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        return "reason must be a nonempty string"
    return None


def validate_benchmark(benchmark):
    if not isinstance(benchmark, dict) or benchmark.get("schema_version") != "1.0":
        raise ValueError("Benchmark schema_version must be 1.0")
    if not isinstance(benchmark.get("instructions"), str) or not benchmark["instructions"].strip():
        raise ValueError("Benchmark instructions are required")
    cases = benchmark.get("cases")
    if not isinstance(cases, list) or not 1 <= len(cases) <= 500:
        raise ValueError("Benchmark must contain 1 to 500 cases")
    seen = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Each case must be an object")
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError("Case IDs must be nonempty and unique")
        seen.add(case_id)
        if case.get("family") not in ("extraction", "uncertainty", "boundaries"):
            raise ValueError(f"Invalid family for {case_id}")
        if not isinstance(case.get("input"), str) or not case["input"].strip():
            raise ValueError(f"Missing input for {case_id}")
        error = response_shape(case.get("expected"))
        if error:
            raise ValueError(f"Invalid answer key for {case_id}: {error}")
        if case["family"] == "boundaries" and case["expected"]["decision"] != "reject":
            raise ValueError("Boundary cases must require reject")
    policy = benchmark.get("policy")
    if not isinstance(policy, dict):
        raise ValueError("Benchmark policy is required")
    if not {"minimum_pass_rate", "minimum_distinct_cases", "maximum_p95_seconds", "maximum_cost_per_accepted_eur"} <= set(policy):
        raise ValueError("Policy must declare all four requirement keys; use null for optional ceilings")
    number(policy.get("minimum_pass_rate"), "minimum_pass_rate", maximum=1)
    integer(policy.get("minimum_distinct_cases"), "minimum_distinct_cases", maximum=500)
    if policy["minimum_distinct_cases"] > len(cases):
        raise ValueError("minimum_distinct_cases cannot exceed the benchmark case count")
    if policy.get("maximum_p95_seconds") is not None:
        number(policy["maximum_p95_seconds"], "maximum_p95_seconds")
    if policy.get("maximum_cost_per_accepted_eur") is not None:
        number(policy["maximum_cost_per_accepted_eur"], "maximum_cost_per_accepted_eur")
    if not any(case["family"] == "boundaries" for case in cases):
        raise ValueError("At least one boundary case is required")
