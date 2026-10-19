# Publication follow-up — 19 October 2026

## Latest disclosure preparation

The subsequent [disclosure review](DISCLOSURE_REVIEW.md) covers Git history,
Actions logs, GitHub text surfaces and completed branch cleanup. It preserves
the evidence chain and records the remaining publication/deployment boundaries.
The dated findings below retain their original implementation-review scope.

## Scope and current status

This follow-up addresses the owner's request to correct the llm-eval decoder failure and remove obsolete license-pending statements. It follows a read-only publication audit and an independent Claude Code review requested with `claude-fable-5-1`. The actual review completed without a fallback selector and included its ending. This records the adapter's selector, not independent attestation of the model provider or backend. The external reviewer assessed supplied material; implementing-agent checks are recorded separately. No model was called by regression tests.

The owner-selected [Noncommercial Local Use License 1.1.0](../LICENSE.md) is included. Version 1.1.0 adds the owner-approved completed report exception to version 1.0.0; the noncommercial qualifier explicitly applies to copying, display and distribution, not just report presentation. README, agent guidance, project metadata and package metadata identify the same license. This resolves the missing-file and inconsistent current-status findings. It does not establish legal enforceability, production fitness or permission to publish the repository. Earlier dated review/test records retain their historical scope; see the dated follow-up in [verification](VERIFICATION.json).

## Rights, presentation and remaining decisions

- **Generated reports — resolved:** section 3 permits noncommercial copying, display and distribution of lawfully generated completed reports, including embedded HTML/CSS, labels and explanatory text. Recipients may further display/share on the same terms. Preserve included notices and identify changes to findings. Template/component extraction and software redistribution are not permitted by this exception; third-party rights remain unaffected. Check confidentiality and data rights before sharing.
- **Business evaluation:** the present license treats evaluation preparing a commercial application as commercial use. A company cannot infer free execution rights from a runnable demo. A limited evaluation exception would require an explicit additional grant; none is implied here.
- **Contributions:** private qualifying local modifications are permitted. Public modified copies and patches containing protected repository material need permission beyond the reserved platform/statutory rights. Contribution workflow and any commercial relicensing permission should be agreed before accepting code. Issue reports with synthetic reproductions are welcome.
- **Commercial delivery:** no published price, checkout or automated license fulfillment exists. An inquiry or payment alone does not grant rights. The repository is source-available, not open source.

## Repository-specific findings

### Corrected decoder-depth failure

An individually bounded model response with 100,000 nested arrays reproduced a `RecursionError` in the JSON decoder. Both raw JSON and fenced diagnostic JSON aborted `evaluate`; the CLI returned a structured input-error object instead of a completed report. The grader now catches decoder recursion failures at both parse sites, counts the attempt as `invalid_json`, and continues evaluating the remaining records and configurations. Saved response bytes, fingerprints and denominators are preserved. A failed attempt is not silently removed or retried.

Three focused regression methods cover raw/fenced grading, unchanged other attempts/configurations and the end-to-end CLI report. Two grading tests were observed failing against the old implementation before the fix. Normal CLI exit 0 means the evaluation completed, not that every attempt passed. `--require-candidate` retains its documented meaning.

### Model provenance supplemented; evaluator and model rights are separate

The [dated artifact provenance supplement](../evidence/local-smoke-2026-10-15/PROVENANCE.md) identifies the manifest, quantized-file and license-text SHA-256 digests for `qwen2.5:3b-instruct-q4_K_M` and `qwen3:8b`. Historical metadata and an August inventory agree with the current manifests; full-file hashing verifies the current weight files against the historical references. Captured license text identifies Qwen Research and Apache-2.0 respectively. This corrects the previous incomplete description of the available artifact evidence. Original download details, exact upstream revisions and independent attestation of historical execution remain unestablished. Existing responses, failures and reports remain unchanged.

The license chosen for the author's evaluation software is separate from the licenses of the models used to collect example responses. Commercial licensing of those example models is not a prerequisite for choosing or separately licensing the author's own evaluator. That choice grants no model-use rights. This repository distributes no model weights, and offline report replay does not invoke a model. Applicable model terms govern new live collection; third-party report/data rights are assessed separately.

### Corrected input-read limit

The local JSON reader now reads at most `MAX_FILE_BYTES + 1` bytes and rejects overflow before UTF-8 decoding or JSON parsing. The initial size check remains an early rejection, not the only guard. This bounds the file payload read when a file grows or its metadata understates its content; it does not bound total parser memory or processing time. Regression checks cover growth after a small initial size, an exact-limit file and one byte over the limit.

### Practical follow-up for the measured model evidence

The capture is usable as a transparently limited historical reference; no new benchmark is needed for the provenance supplement. Retain the recovered identifiers alongside the original evidence and describe the remaining reconstruction limits without retroactively changing the run. Any additional historical receipt can be added as separately dated evidence after verification. Model terms remain separate from the evaluator license. See the [provenance checklist](PROVENANCE.md#model-artifact-and-rights-checklist).

The 18 measured responses on nine authored tasks remain a bounded reference case, not a representative benchmark or a deployment recommendation. No new model or measurement was added.
