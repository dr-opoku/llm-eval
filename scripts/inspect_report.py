"""Inspect declared sample eligibility; never authorize an action or authenticate evidence."""
import argparse
import json
import math
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError("Nonfinite number: " + value)


def finite_float(value):
    number = float(value)
    require(math.isfinite(number), "Nonfinite JSON number")
    return number


def inspect_report(report):
    require(isinstance(report, dict) and report.get("schema_version") == "1.0", "Unsupported report")
    if report.get("status") == "error":
        return {"assessment": "input_error", "source_verified_by_consumer": False, "action_authorized": False}
    require(report.get("deployment_readiness") == "not_established", "Unexpected deployment claim")
    provenance = report.get("provenance")
    require(isinstance(provenance, dict) and provenance.get("kind") in ("synthetic", "measured", "imported"), "Missing provenance")
    expected_scope = "illustrative" if provenance["kind"] == "synthetic" else "supplied_task_sample_only"
    require(report.get("evidence_scope") == expected_scope, "Unexpected scope")
    for key in ("benchmark_sha256", "run_sha256"):
        value = report.get(key)
        require(isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value), "Missing content identity")
    policy = report.get("policy")
    require(isinstance(policy, dict), "Missing policy")
    for key in ("minimum_pass_rate", "minimum_distinct_cases", "maximum_p95_seconds", "maximum_cost_per_accepted_eur"):
        require(key in policy, "Missing requirement")
    require(type(policy["minimum_distinct_cases"]) is int and 1 <= policy["minimum_distinct_cases"] <= 500, "Invalid sample minimum")
    value = policy["minimum_pass_rate"]
    require(type(value) in (int, float) and 0 <= value <= 1, "Invalid acceptance target")
    for key in ("maximum_p95_seconds", "maximum_cost_per_accepted_eur"):
        value = policy[key]
        require(value is None or (type(value) in (int, float) and 0 <= value <= 1e308 and math.isfinite(value)), "Invalid ceiling")
    configurations = report.get("configurations")
    require(isinstance(configurations, list) and 1 <= len(configurations) <= 20, "Missing configurations")
    ids, candidates, outcomes = set(), [], []
    for item in configurations:
        require(isinstance(item, dict), "Invalid configuration")
        identity = item.get("configuration_id")
        require(isinstance(identity, str) and identity and identity not in ids, "Invalid or duplicate configuration ID")
        ids.add(identity)
        checks = item.get("checks")
        names = {"matrix_complete", "distinct_case_minimum", "case_acceptance", "boundary_cases", "latency", "cost"}
        require(isinstance(checks, dict) and set(checks) == names, "Missing or unknown checks")
        require(all(isinstance(v, str) and v in {"pass", "fail", "unknown", "not_required"} for v in checks.values()), "Invalid check verdict")
        require(all(checks[k] != "not_required" for k in names - {"latency", "cost"}), "Mandatory check disabled")
        for check, key in (("latency", "maximum_p95_seconds"), ("cost", "maximum_cost_per_accepted_eur")):
            require((checks[check] == "not_required") == (policy[key] is None), "Optional check contradicts policy")
        for key in ("observed_records", "expected_records", "missing_records", "distinct_cases", "accepted_records", "execution_errors", "boundary_requirement_failures"):
            require(type(item.get(key)) is int and item[key] >= 0, "Missing or invalid denominator")
        observed, expected, accepted = (item[k] for k in ("observed_records", "expected_records", "accepted_records"))
        require(0 < expected <= 10_000 and 0 <= accepted <= observed <= expected and item["missing_records"] == expected - observed, "Inconsistent record counts")
        require(0 <= item["distinct_cases"] <= observed and accepted + item["execution_errors"] <= observed and item["boundary_requirement_failures"] <= observed, "Inconsistent observations")
        require(checks["matrix_complete"] == ("pass" if observed == expected else "unknown"), "Inconsistent matrix verdict")
        require(checks["distinct_case_minimum"] == ("pass" if item["distinct_cases"] >= policy["minimum_distinct_cases"] else "unknown"), "Inconsistent distinct-case verdict")
        require(checks["case_acceptance"] == ("pass" if accepted / expected >= policy["minimum_pass_rate"] else "fail"), "Inconsistent acceptance verdict")
        if item["boundary_requirement_failures"]:
            require(checks["boundary_cases"] == "fail", "Boundary failure hidden")
        if checks["matrix_complete"] == "pass":
            require(checks["boundary_cases"] == ("fail" if item["boundary_requirement_failures"] else "pass"), "Inconsistent boundary verdict")
        for check, key, metric in (("latency", "maximum_p95_seconds", "p95_seconds"), ("cost", "maximum_cost_per_accepted_eur", "cost_per_accepted_eur")):
            details = item.get(check)
            require(isinstance(details, dict) and type(details.get("complete")) is bool, "Missing measurement coverage")
            count = details.get("observations")
            require(type(count) is int and 0 <= count <= observed and details["complete"] == (observed == expected and count == expected), "Inconsistent measurement coverage")
            value = details.get(metric)
            require(value is None or (type(value) in (int, float) and 0 <= value <= 1e308 and math.isfinite(value)), "Invalid measurement")
            require(not details["complete"] or value is not None or (check == "cost" and accepted == 0), "Complete measurement has no value")
            require(not (check == "cost" and accepted == 0) or value is None, "Undefined cost ratio must be null")
            if policy[key] is not None:
                verdict = "unknown" if not details["complete"] else ("fail" if check == "cost" and accepted == 0 else ("pass" if value is not None and value <= policy[key] else "fail"))
                require(checks[check] == verdict, "Measurement verdict contradicts coverage or ceiling")
        outcome = "insufficient_evidence" if "unknown" in checks.values() else ("does_not_meet_sample_rules" if "fail" in checks.values() else "meets_sample_rules")
        require(item.get("outcome") == outcome, "Aggregate contradicts checks")
        outcomes.append(outcome)
        if outcome == "meets_sample_rules":
            candidates.append(identity)
    selection = report.get("selection")
    require(isinstance(selection, dict) and selection.get("automatic_winner", "missing") is None and selection.get("candidate_ids") == candidates, "Invalid selection")
    return {"assessment": "sample_rules_met" if candidates else ("insufficient_evidence" if "insufficient_evidence" in outcomes else "criteria_not_met"),
            "candidate_ids": candidates, "evidence_scope": expected_scope,
            "source_verified_by_consumer": False, "action_authorized": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="JSON file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        if args.report == "-":
            raw = sys.stdin.buffer.read(20_000_001)
        else:
            with Path(args.report).open("rb") as stream:
                raw = stream.read(20_000_001)
        require(len(raw) <= 20_000_000, "Report exceeds 20 MB")
        report = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid_constant, parse_float=finite_float)
        result = inspect_report(report)
        code = 2 if result["assessment"] == "input_error" else (0 if result["assessment"] == "sample_rules_met" else 1)
    except (ValueError, OSError, TypeError, KeyError, OverflowError, RecursionError) as exc:
        result = {"assessment": "invalid_report", "message": str(exc), "source_verified_by_consumer": False, "action_authorized": False}
        code = 2
    print(json.dumps(result, allow_nan=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
