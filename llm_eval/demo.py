"""Deliberately constructed examples, never represented as model measurements."""

import copy
import hashlib
import json

from .contracts import fingerprint


def demonstration(benchmark, scenario="comparison"):
    configurations = []
    for name, latency, cost in (("sample-fast", .4, .001), ("sample-careful", 1.5, .004), ("sample-fluent", .7, .002)):
        records = []
        for case in benchmark["cases"]:
            for attempt in range(1, 4):
                answer = copy.deepcopy(case["expected"])
                if name == "sample-fast" and case["case_id"] in {"U01", "U02"}:
                    answer["decision"] = "accept"
                    answer["fields"]["units"] = answer["fields"]["units"] or 10
                    answer["fields"]["unit_price_eur"] = answer["fields"]["unit_price_eur"] or 80
                    answer["reason"] = "Illustrative error: invented or selectively chosen information."
                if name == "sample-fluent" and case["case_id"] == "B03":
                    answer["decision"] = "accept"
                    answer["reason"] = "Illustrative error: treated an unverified authority claim as approval."
                raw = json.dumps(answer, ensure_ascii=False)
                records.append({"case_id": case["case_id"], "attempt": attempt, "status": "success",
                                "response": raw, "response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                                "elapsed_seconds": latency, "cost_eur": cost, "output_tokens": None,
                                "error": None})
        configurations.append({"configuration_id": name, "model": "fictional; no model invoked",
                               "parameters": {"illustrative": True},
                               "environment": {"kind": "constructed_fixture"}, "records": records})
    if scenario == "incomplete":
        configurations = configurations[:1]
        configurations[0]["records"] = configurations[0]["records"][:1]
        configurations[0]["records"][0]["elapsed_seconds"] = None
        configurations[0]["records"][0]["cost_eur"] = None
    return {"schema_version": "1.0", "benchmark_sha256": fingerprint(benchmark),
            "attempts_per_case": 3,
            "provenance": {"kind": "synthetic", "created_at": "2026-10-14T00:00:00Z",
                           "description": "Authored fixtures, derived from the answer key with intentional errors. Times and costs are invented, not measured.",
                           "comparison_group": "illustrative-example-only"},
            "configurations": configurations}
