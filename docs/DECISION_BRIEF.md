# Decision brief: a completed bounded reference case

**Question:** Can either of the two captured local configurations satisfy the fictional purchasing desk's declared supplier-triage requirements?

**Recorded decision:** Neither configuration meets every frozen sample requirement. Do not nominate an automatic winner. This completes the reference case's decision narrative; it does not establish readiness for a real procurement or deployment.

## What was evaluated

The existing [capture](../evidence/local-smoke-2026-10-15/README.md) contains 18 measured responses: nine authored public cases, one attempt per case for each of two already installed configurations. Cases cover extraction, missing/conflicting information and untrusted authority claims. The task data and answer key are synthetic; the responses and request timings are measured. `accept` is a triage label, not permission to place orders or pay.

The [benchmark and policy](../evidence/local-smoke-2026-10-15/benchmark.json) were fixed before that capture: at least 85% accepted attempts, all mandatory boundary cells accepted, nine distinct cases and full-request p95 no more than 3.0 seconds. No cost ceiling was required. Finalization adds no model, attempt, changed policy or replacement response to that evidence.

## What the existing evidence supports

| Recorded configuration | Accepted / attempts | Failing boundary cells | Request p95 | Required checks that fail |
| --- | --- | --- | --- | --- |
| `qwen2.5:3b-instruct-q4_K_M` | 2/9 | 3 | 9.010349 s | Acceptance, boundaries, latency |
| `qwen3:8b` | 8/9 | 0 | 20.787311 s | Latency |

All 18 requests completed without execution errors. Rejected answers remain in the [complete run](../evidence/local-smoke-2026-10-15/run.json). A boundary failure can be a formatting/content failure, not necessarily an unauthorized proposed decision; inspect the per-attempt reason codes in the [report](../evidence/local-smoke-2026-10-15/report.json). The second configuration meets the sample's answer and boundary requirements but misses the declared operating requirement. Requirements were not relaxed after seeing the results.

## Decision consequence and accountability

This fictional case supports retaining review of the proposed triage output rather than claiming qualified automation. It does not show that either configuration is generally unsuitable: the result is specific to these settings, cases and request-timing definition.

For an actual assignment, the business owner would confirm the triage boundary and service expectation; a technical lead would check the measurement design and configuration; the project/program lead would record unresolved requirements and the next decision. These are proposed responsibilities, not claims about a delivered customer project.

If a real use case warrants further work, preregister a separate evaluation using the [evaluation protocol](EVALUATION_PROTOCOL.md). Different latency definitions, warm-model operation or configuration changes require a separately labeled run. They must not replace this capture or silently change its verdict. Further experiments are not required to understand this completed reference case.

## Limits that matter

- Nine public authored cases and one attempt per configuration/case do not establish representative or statistically reliable performance; there is no independent holdout.
- Request time includes model loading with `keep_alive=0`. Configuration order was fixed and host load was uncontrolled. This is not an equalized hardware study or a general model-family ranking.
- Costs and human work time were not measured. No financial comparison, labor-saving claim or cost advantage follows.
- Model tags and reduced metadata were recorded; weight identity was not independently authenticated.
- Free-form reason truth is not graded. Proposed boundary decisions do not test actual tool permissions or enforced authorization.
- Later operational checks and separately staged model downloads are outside this reference evidence. They do not establish that the captured configurations are current market leaders or obsolete.

## Inspect and replay without a model

Read the [saved text](../evidence/local-smoke-2026-10-15/report.txt), or download/open the [standalone HTML](../evidence/local-smoke-2026-10-15/report.html). From the checkout:

```bash
python3 -m llm_eval evaluate evidence/local-smoke-2026-10-15/run.json \
  --benchmark evidence/local-smoke-2026-10-15/benchmark.json --format json
python3 scripts/reproduce_examples.py --check
```

Evaluation exits 0 when successfully computed, even when no configuration qualifies. Add `--require-candidate` to receive exit 1 for this negative sample result. No model call is made by these commands.

## Why this is a professional reference

The demonstrated contribution is connecting a business task to explicit acceptance criteria, retaining failed observations, distinguishing answer quality from operating requirements and making the decision inspectable by people and agents. The compact implementation is reproducible, not a claim of a complexity moat. Enterprise transformation outcomes, adoption and commercial demand require separate evidence.

The reference narrative is complete within its stated scope. Usage rights, public release and any commercial offer remain separate [owner decisions](PROJECT_STATUS.md); this document grants no license.
