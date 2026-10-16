# Protocol for an independent task-specific decision

This is a protocol template for future work, **not a completed evaluation**. The bundled examples and local smoke run do not satisfy it.

## Before collecting the decision sample

1. Name the decision and accountable business owner: adopt, investigate, buy, build or defer, within a stated scope. Define the cost of consequential mistakes and which requirements are mandatory.
2. Freeze the task contract, label vocabulary, exact grading rules, boundary cases and handling of missing/failed outputs. Have domain reviewers independently assess answer keys and adjudicate disagreements; record that process without publishing private data.
3. Separate development tasks from a held-out decision sample. Freeze immutable case IDs, deduplication rules and an independent task-family sampling plan. Repeated calls to one case do not create new independent tasks. Select sample size from decision risk and required precision, not the nine-case fixture.
4. Freeze candidate model/weight identity, quantization, adapter/prompt, serving version, parameters and human intervention policy. Record which configurations were tuned on development tasks; no tuning on holdout outcomes.
5. Freeze acceptance rate, distinct-case minimum, boundary requirements and any cost/latency ceilings. A minimum cannot exceed the benchmark's distinct cases. Optional criteria must be explicitly null before collection; unknown accounting cannot pass a required cost check.
6. Define comparable operating conditions: warm/cold service, concurrency, context/output budgets, hardware/placement, timing boundary and load monitoring. Randomize or counterbalance order where relevant. Record deviations.
7. Define a common monetary/time budget and cost allocation: successful/failed calls, retries, probes, infrastructure, licenses and human work. Log actual human minutes and intervention counts by activity. The current runner does not measure these costs or human effort automatically.

## During collection

Retain the entire declared attempt matrix, raw responses, failures, timestamps, version metadata, request/response hashes and the frozen benchmark. Never replace a failed attempt with a successful retry. Stop rules and missing-data treatment must be fixed in advance. Keep sensitive corpora and captures private; publish only inspected, permissioned evidence.

## After collection

Recompute grades independently where feasible; inspect disagreements and consequential errors. Report denominators by task family, missing evidence, distributions and appropriate uncertainty, with analysis at the independent task level. The current engine supplies counts and nearest-rank p95 only; it does not implement a statistical study or a human adjudication system.

Preserve the original policy. Any later interpretation under another policy must be labeled as a separate analysis and identify the original evidence. Compare build/buy alternatives on maintenance, integration effort, governance, adoption and expected business outcome as well as answer quality. Eligibility in this sample cannot authorize a transaction, tool action or deployment.

Deliver the protocol, complete evidence, analysis, decisions, unresolved risks and accountable next steps. A real pilot and organizational acceptance need additional evidence beyond this repository.
