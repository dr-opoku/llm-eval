# Data contract, version 1.0

Inputs and outputs are UTF-8 JSON. The project-specific contracts are described here and in [schemas](schemas/). The runtime uses its own focused validation, not a third-party JSON Schema validator. Extra run metadata is preserved by the run fingerprint but not automatically checked or interpreted.

File input is limited to 20 MB. Answer strings are limited to one million characters. Duplicate JSON object keys are rejected. Numbers used in metrics must be finite and nonnegative; booleans are not numbers. No caller-provided path is opened during response grading.

## Benchmark

Use [the bundled benchmark](../llm_eval/fixtures/benchmark.json) as the complete example.

Required keys: `schema_version`, `instructions`, `policy`, `cases`. `benchmark_id` and `description` are recommended. Cases have unique `case_id`, `family` (`extraction`, `uncertainty`, `boundaries`), `input` and `expected`. Expected answers use the same shape required of model responses. Every benchmark must include a boundary case, and its expected decision must be reject.

Policy keys:

| Key | Meaning |
| --- | --- |
| `minimum_pass_rate` | Required share of accepted expected cells, from 0 to 1 |
| `minimum_distinct_cases` | Minimum distinct supplied cases, from 1 to 500 |
| `maximum_p95_seconds` | Optional latency ceiling; null disables this requirement |
| `maximum_cost_per_accepted_eur` | Optional cost ceiling; null disables this requirement |

## Response

```json
{
  "decision": "review",
  "fields": {"supplier": "Cedar Demo Ltd", "units": null, "unit_price_eur": 12.5},
  "evidence_ids": ["S1"],
  "reason": "Quantity has not been supplied."
}
```

All four top-level keys and all three field keys are required; additional response keys are rejected. Supplier is a nonempty string or null. Units is an integer from 1 to 1,000,000 or null. Unit price is a finite number from 0 to 1,000,000 or null. Evidence IDs are nonempty unique strings. Reason is a nonempty string. Evidence ID order does not matter; extra or omitted IDs fail the exact evidence match.

## Run

The complete [illustrative run](../examples/illustrative-run.json) is explicitly synthetic. To import a real run, set `provenance.kind` to `measured` for direct capture or `imported` for externally supplied records and describe the collector, dates and cost source.

```json
{
  "schema_version": "1.0",
  "benchmark_sha256": "CANONICAL_BENCHMARK_SHA256",
  "attempts_per_case": 1,
  "provenance": {"kind": "imported", "description": "Describe collection conditions here."},
  "configurations": [
    {
      "configuration_id": "configured-model-a",
      "model": "actual-model-label",
      "parameters": {"temperature": 0},
      "environment": {"adapter": "your-adapter", "cost_source": "your-accounting-source"},
      "records": [
        {
          "case_id": "E01", "attempt": 1, "status": "success",
          "response": "{\"decision\":\"accept\",\"fields\":{\"supplier\":\"Cedar Demo Ltd\",\"units\":20,\"unit_price_eur\":12.5},\"evidence_ids\":[\"S1\"],\"reason\":\"Complete request.\"}",
          "elapsed_seconds": 0.8, "cost_eur": null, "output_tokens": null
        }
      ]
    }
  ]
}
```

The example is intentionally incomplete and therefore cannot establish sample-rule eligibility. Replace the fingerprint placeholder with `llm_eval.contracts.fingerprint(benchmark_dict)`.

- One to 20 unique configurations; one to 20 declared attempts per case.
- Record status is success or error. An error still needs a response string, normally empty.
- Elapsed time, cost and output token count can be null or omitted; missing measurements are not zero.
- `response_sha256` is optional for imports; if supplied, it must match the complete response string.
- Collector-specific request objects, raw transport, mode probes, timing details and environment metadata may be included. Do not fabricate unavailable fields.
- A fingerprint verifies correspondence with the supplied task, not a trustworthy timestamp, source or author.

## Report

Reports include the benchmark and run fingerprints, original provenance, declared policy, evidence scope, deployment readiness, candidate list, per-configuration checks, denominators, cost/timing coverage and per-attempt results. Report version is independent of any vendor API version.

`deployment_readiness` is always `not_established`. For synthetic runs `evidence_scope` is `illustrative`; for measured/imported runs it is `supplied_task_sample_only`. No statistical representativeness or external authenticity is inferred.
