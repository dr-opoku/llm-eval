# Measurement rules

## 1. Freeze the task before comparing configurations

The benchmark combines instructions, case inputs, an explicit answer key and business requirements. Its canonical SHA-256 identifies the entire object. Any change, including a policy change, creates a different fingerprint. Keep the previous object if you want to reinterpret earlier responses; document the change rather than silently relabeling an old run.

The runner sends only instructions and case inputs to the model. Expected answers and the selection policy are never included in live prompts. The benchmark is public, so it is not an unseen evaluation set and cannot support a claim about generalization.

## 2. Distinguish transport from acceptance

`status=success` means the collection process received a completed response. Acceptance additionally requires every case gate:

| Gate | Operation | Limit |
| --- | --- | --- |
| Strict JSON | Parse the entire trimmed response with duplicate-key and non-finite-constant rejection | No prose, repair or Markdown wrapper |
| Shape | Exactly the declared keys, field types and decision vocabulary | No general JSON Schema validator dependency |
| Fields | Compare the supplied fields with the frozen expected fields | Exact value matching; numeric 80 and 80.0 are equivalent, booleans are excluded |
| Decision | Compare accept/review/reject with the frozen label | accept is a triage label, never purchase approval |
| Evidence | Compare the set of evidence IDs with the expected set | Referencing a source does not establish that it is true |

Reason text must be nonempty. Its factual correctness is not evaluated. Code-fenced JSON may receive diagnostic field/decision/evidence results, but strict JSON remains false and the attempt fails. Malformed objects, arrays, duplicate keys and invalid field types fail without being repaired.

## 3. Report denominators and missing cells

An attempt cell is `(configuration_id, case_id, attempt)`. The expected matrix has `distinct benchmark cases × declared attempts_per_case` cells per configuration. Duplicate cells and unknown cases are input errors, not additional evidence. Missing cells remain missing. Transport errors count as observed failed attempts.

- Observed acceptance: accepted / supplied records, or unknown if none.
- Matrix acceptance: accepted / expected cells. Missing cells do not count as accepted.
- A complete matrix and the minimum distinct-case count are mandatory.

The bundled minimum is nine distinct cases. It is an example coverage rule, not a minimum scientifically adequate sample size. The default three attempts use the same seed; they do not establish independent observations. No confidence interval, significance test or population estimate is produced.

## 4. Apply mandatory requirements separately

The default policy requires at least 85% matrix acceptance, all boundary cells accepted and a full-matrix p95 request time of at most three seconds. These values are illustrative. Boundary failures cannot be offset by successes elsewhere.

Here a boundary requirement failure means ANY failed gate on a boundary case, including a malformed response or transport error. It does not always mean the model granted unauthorized rights. Inspect per-attempt reason codes for the actual failure.

`insufficient_evidence` takes precedence if a required check is unknown. Known failures still appear in the checks and counts. With complete required evidence, any failed check yields `does_not_meet_sample_rules`; otherwise the configuration `meets_sample_rules`.

## 5. Define latency and cost scope

Mean and p95 use all supplied finite nonnegative full-request durations, including errors. p95 is the nearest-rank value at `ceil(0.95 × n)`, not an interpolated estimate. Partial timing samples are displayed with their count but cannot pass a required latency check.

The local runner uses `keep_alive=0`. Request time includes loading, generation, transfer and client overhead; it is not pure decoding speed. Available Ollama load and evaluation durations remain in run records. Probe and inventory requests are excluded. Shared host activity is not controlled or continuously instrumented, so performance comparisons require operator review.

Cost per accepted result is **the sum of supplied costs for ALL declared attempt cells divided by accepted attempts**. It is unknown if any cell/cost is missing or no result is accepted. Failure costs are included. This metric excludes setup, probes, development labor and any expenses not supplied; it is not total cost of ownership. Cost is EUR only; no currency conversion is performed. Actual cost provenance belongs in the run metadata. A task retry consumes a separate attempt cell; no failed cell may be replaced by a successful retry.

## 6. Keep eligibility separate from procurement

The report provides candidate IDs, with no automatic winner. Model weights/quantization, adapter instructions, context allocation, hardware, host load, timing scope and cost accounting must be comparable before a purchasing conclusion is drawn. A model label is not a verified model identity.

For a real decision add representative held-out tasks, independent review of answer keys, actual prices, deployment requirements and separate authorization/tool-execution checks. No benchmark score authorizes an agent to act.
