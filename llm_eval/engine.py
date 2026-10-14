"""Evaluate observed attempts without repairing output or inferring ground truth."""

import hashlib
import math
import re
from collections import Counter

from .contracts import (
    MAX_RESPONSE_CHARS, fingerprint, integer, number, parse_json,
    response_shape, validate_benchmark,
)


def grade(case, raw):
    result = {"strict_json": False, "schema_valid": False, "fields_match": None,
              "decision_match": None, "evidence_match": None, "accepted": False,
              "diagnostic_fenced_json": False, "reason_codes": []}
    try:
        parsed = parse_json(raw.strip())
        result["strict_json"] = True
    except ValueError:
        fence = re.fullmatch(r"\s*```(?:json)?\s*(\{.*\})\s*```\s*", raw, re.S | re.I)
        if fence:
            try:
                parsed = parse_json(fence.group(1))
                result["diagnostic_fenced_json"] = True
            except ValueError:
                result["reason_codes"].append("invalid_json")
                return result
        else:
            result["reason_codes"].append("invalid_json")
            return result
    if not result["strict_json"]:
        result["reason_codes"].append("non_strict_json")
    error = response_shape(parsed)
    if error:
        result["reason_codes"].append("invalid_schema")
        result["schema_error"] = error
        return result
    result["schema_valid"] = True
    expected = case["expected"]
    result["fields_match"] = parsed["fields"] == expected["fields"]
    result["decision_match"] = parsed["decision"] == expected["decision"]
    result["evidence_match"] = set(parsed["evidence_ids"]) == set(expected["evidence_ids"])
    for key in ("fields_match", "decision_match", "evidence_match"):
        if not result[key]:
            result["reason_codes"].append(key + "_failed")
    result["accepted"] = result["strict_json"] and all(
        result[key] for key in ("schema_valid", "fields_match", "decision_match", "evidence_match")
    )
    return result


def _optional_number(value, label):
    if value is not None:
        number(value, label)


def _p95(values):
    return sorted(values)[math.ceil(.95 * len(values)) - 1] if values else None


def evaluate(benchmark, run):
    validate_benchmark(benchmark)
    if not isinstance(run, dict) or run.get("schema_version") != "1.0":
        raise ValueError("Run schema_version must be 1.0")
    if run.get("benchmark_sha256") != fingerprint(benchmark):
        raise ValueError("Run fingerprint does not match this benchmark")
    provenance = run.get("provenance")
    if not isinstance(provenance, dict) or provenance.get("kind") not in ("synthetic", "measured", "imported"):
        raise ValueError("Provenance kind must be synthetic, measured, or imported")
    count = run.get("attempts_per_case")
    integer(count, "attempts_per_case", maximum=20)
    configs = run.get("configurations")
    if not isinstance(configs, list) or not 1 <= len(configs) <= 20:
        raise ValueError("Run must contain 1 to 20 configurations")
    cases = {case["case_id"]: case for case in benchmark["cases"]}
    expected_count = len(cases) * count
    policy = benchmark["policy"]
    summaries = []
    seen_configs = set()
    for config in configs:
        if not isinstance(config, dict):
            raise ValueError("Each configuration must be an object")
        config_id = config.get("configuration_id")
        if not isinstance(config_id, str) or not config_id or config_id in seen_configs:
            raise ValueError("Configuration IDs must be nonempty and unique")
        seen_configs.add(config_id)
        if config.get("model") is not None and not isinstance(config["model"], str):
            raise ValueError("Model label must be a string or null")
        if any(not isinstance(config.get(key, {}), dict) for key in ("parameters", "environment")):
            raise ValueError("Parameters and environment must be objects")
        records = config.get("records")
        if not isinstance(records, list) or len(records) > expected_count:
            raise ValueError("Records must be a list no larger than the declared matrix")
        cells = set()
        graded = []
        for record in records:
            if (not isinstance(record, dict) or not isinstance(record.get("case_id"), str)
                    or record["case_id"] not in cases):
                raise ValueError("Unknown or missing case_id in record")
            integer(record.get("attempt"), "attempt", maximum=count)
            cell = (record["case_id"], record["attempt"])
            if cell in cells:
                raise ValueError(f"Duplicate attempt cell: {cell}")
            cells.add(cell)
            if record.get("status") not in ("success", "error"):
                raise ValueError("Record status must be success or error")
            raw = record.get("response")
            if not isinstance(raw, str) or len(raw) > MAX_RESPONSE_CHARS:
                raise ValueError("Response must be a bounded string")
            for key in ("elapsed_seconds", "cost_eur"):
                _optional_number(record.get(key), key)
            tokens = record.get("output_tokens")
            if tokens is not None:
                integer(tokens, "output_tokens", minimum=0, maximum=100_000_000)
            raw_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if record.get("response_sha256") not in (None, raw_hash):
                raise ValueError("Response fingerprint mismatch")
            if record["status"] == "error":
                verdict = {"accepted": False, "strict_json": False, "schema_valid": False,
                           "fields_match": None, "decision_match": None, "evidence_match": None,
                           "diagnostic_fenced_json": False, "reason_codes": ["execution_error"]}
            else:
                verdict = grade(cases[record["case_id"]], raw)
            graded.append({"case_id": record["case_id"], "attempt": record["attempt"],
                           "family": cases[record["case_id"]]["family"],
                           "response_sha256": raw_hash, "status": record["status"], **verdict})
        accepted = sum(row["accepted"] for row in graded)
        errors = sum(row["status"] == "error" for row in graded)
        distinct = len({row["case_id"] for row in graded})
        complete = len(cells) == expected_count
        timings = [record["elapsed_seconds"] for record in records if record.get("elapsed_seconds") is not None]
        costs = [record["cost_eur"] for record in records if record.get("cost_eur") is not None]
        latency_complete = complete and len(timings) == expected_count
        cost_complete = complete and len(costs) == expected_count
        p95 = _p95(timings)
        cost_per_accepted = sum(costs) / accepted if cost_complete and accepted else None
        boundary = [row for row in graded if row["family"] == "boundaries"]
        boundary_expected = count * sum(case["family"] == "boundaries" for case in cases.values())
        boundary_failures = sum(not row["accepted"] for row in boundary)
        checks = {
            "matrix_complete": "pass" if complete else "unknown",
            "distinct_case_minimum": "pass" if distinct >= policy["minimum_distinct_cases"] else "unknown",
            "case_acceptance": "pass" if accepted / expected_count >= policy["minimum_pass_rate"] else "fail",
            "boundary_cases": "fail" if boundary_failures else ("pass" if len(boundary) == boundary_expected else "unknown"),
            "latency": "not_required",
            "cost": "not_required",
        }
        if policy["maximum_p95_seconds"] is not None:
            checks["latency"] = ("pass" if p95 <= policy["maximum_p95_seconds"] else "fail") if latency_complete else "unknown"
        if policy["maximum_cost_per_accepted_eur"] is not None:
            checks["cost"] = ("pass" if cost_per_accepted <= policy["maximum_cost_per_accepted_eur"] else "fail") if cost_per_accepted is not None else "unknown"
        # Missing evidence takes precedence over a partial-sample aggregate verdict.
        outcome = "insufficient_evidence" if "unknown" in checks.values() else (
            "does_not_meet_sample_rules" if "fail" in checks.values() else "meets_sample_rules"
        )
        summaries.append({
            "configuration_id": config_id, "model": config.get("model"),
            "parameters": config.get("parameters", {}), "environment": config.get("environment", {}),
            "outcome": outcome, "checks": checks,
            "observed_records": len(records), "expected_records": expected_count,
            "missing_records": expected_count - len(records), "distinct_cases": distinct,
            "accepted_records": accepted, "execution_errors": errors,
            "observed_acceptance_rate": accepted / len(records) if records else None,
            "matrix_acceptance_rate": accepted / expected_count,
            "strict_json_records": sum(row["strict_json"] for row in graded),
            "boundary_requirement_failures": boundary_failures,
            "reason_counts": dict(sorted(Counter(code for row in graded for code in row["reason_codes"]).items())),
            "latency": {"observations": len(timings), "complete": latency_complete,
                        "mean_seconds": sum(timings) / len(timings) if timings else None, "p95_seconds": p95},
            "cost": {"observations": len(costs), "complete": cost_complete,
                     "observed_total_eur": sum(costs) if costs else None,
                     "cost_per_accepted_eur": cost_per_accepted},
            "cases": graded,
        })
    return {
        "schema_version": "1.0", "benchmark_id": benchmark.get("benchmark_id"),
        "benchmark_sha256": fingerprint(benchmark), "run_sha256": fingerprint(run),
        "provenance": provenance, "policy": policy,
        "evidence_scope": "illustrative" if provenance["kind"] == "synthetic" else "supplied_task_sample_only",
        "deployment_readiness": "not_established",
        "selection": {"candidate_ids": [item["configuration_id"] for item in summaries if item["outcome"] == "meets_sample_rules"],
                      "automatic_winner": None,
                      "reason": "Sample-rule eligibility is not a production recommendation or a causal model ranking."},
        "configurations": summaries,
        "limitations": [
            "Exact labels, fields and evidence IDs are checked; the explanation's truth is not graded.",
            "Boundary cases examine proposed decisions, not executed tools or enforced authorization.",
            "Repeated attempts on the same cases do not establish independent or representative evidence.",
            "Reported timing and supplied costs are configuration-specific; comparability requires review.",
            "Fingerprints establish content identity, not authorship, external authenticity or truth.",
        ],
    }
