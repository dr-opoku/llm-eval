# Publication follow-up — 19 October 2026

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

### Still present; model provenance needs separate review

The measured example names `qwen2.5:3b-instruct-q4_K_M` and `qwen3:8b`. The upstream [Qwen2.5-3B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) identifies `qwen-research`, while [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) identifies Apache-2.0 (checked 19 October 2026). Do not describe all Qwen models as Apache-licensed. These upstream pages do not attest the exact historical quantized artifact used in the capture. The repository license does not replace model terms; this note does not assert that model-weight terms automatically apply to generated responses. Establishing the historical artifact's provenance and any applicable publication conditions remains a separate task. Existing capture and failure evidence remain unchanged.

### Corrected input-read limit

The local JSON reader now reads at most `MAX_FILE_BYTES + 1` bytes and rejects overflow before UTF-8 decoding or JSON parsing. The initial size check remains an early rejection, not the only guard. This bounds the file payload read when a file grows or its metadata understates its content; it does not bound total parser memory or processing time. Regression checks cover growth after a small initial size, an exact-limit file and one byte over the limit.

### Practical follow-up for the measured model evidence

The capture is usable as a transparently limited historical reference; no new benchmark is needed to document these limits. Before describing this as commercially cleared model evidence, confirm the original use purpose and applicable model permissions, and recover immutable artifact identity/source/license evidence if available. Do not substitute today's installed tag or an unrelated upstream revision for the historical artifact. If no contemporaneous evidence exists, retain the unknown and document it; preserve every original response/failure and do not retroactively relabel the run. Model terms are separate from the evaluator license. See the [provenance checklist](PROVENANCE.md#model-artifact-and-rights-checklist).

The 18 measured responses on nine authored tasks remain a bounded reference case, not a representative benchmark or a deployment recommendation. No new model or measurement was added.
