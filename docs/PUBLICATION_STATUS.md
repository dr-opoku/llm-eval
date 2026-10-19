# Publication follow-up — 19 October 2026

## Scope and current status

This follow-up addresses the owner's request to correct the llm-eval decoder failure and remove obsolete license-pending statements. It follows a read-only publication audit and an independent Claude Code review requested with `claude-fable-5-1`. The actual review completed without a fallback selector and included its ending. This records the adapter's selector, not independent attestation of the model provider or backend. The external reviewer assessed supplied material; implementing-agent checks are recorded separately. No model was called by regression tests.

The owner-selected [Noncommercial Local Use License 1.0.0](../LICENSE.md) is now included unchanged. README, agent guidance, project metadata and package metadata identify the same license. This resolves the missing-file and inconsistent current-status findings. It does not establish legal enforceability, production fitness or permission to publish the repository. Earlier dated review/test records retain their historical scope; see the dated follow-up in [verification](VERIFICATION.json).

## Remaining rights and presentation decisions

- **Generated reports:** HTML templates, styles and software-authored explanatory text are embedded in reports. The current output clause does not expressly permit sharing protected embedded material. A narrowly scoped report-output exception could resolve this without licensing redistribution of the tool; it has not been adopted.
- **Business evaluation:** the present license treats evaluation preparing a commercial application as commercial use. A company cannot infer free execution rights from a runnable demo. A limited evaluation exception would require an explicit additional grant; none is implied here.
- **Contributions:** private qualifying local modifications are permitted. Public modified copies and patches containing protected repository material need permission beyond the reserved platform/statutory rights. Contribution workflow and any commercial relicensing permission should be agreed before accepting code. Issue reports with synthetic reproductions are welcome.
- **Commercial delivery:** no published price, checkout or automated license fulfillment exists. An inquiry or payment alone does not grant rights. The repository is source-available, not open source.

## Repository-specific findings

### Corrected decoder-depth failure

An individually bounded model response with 100,000 nested arrays reproduced a `RecursionError` in the JSON decoder. Both raw JSON and fenced diagnostic JSON aborted `evaluate`; the CLI returned a structured input-error object instead of a completed report. The grader now catches decoder recursion failures at both parse sites, counts the attempt as `invalid_json`, and continues evaluating the remaining records and configurations. Saved response bytes, fingerprints and denominators are preserved. A failed attempt is not silently removed or retried.

Three focused regression methods cover raw/fenced grading, unchanged other attempts/configurations and the end-to-end CLI report. Two grading tests were observed failing against the old implementation before the fix. Normal CLI exit 0 means the evaluation completed, not that every attempt passed. `--require-candidate` retains its documented meaning.

### Still present; model provenance needs separate review

The measured example names `qwen2.5:3b-instruct-q4_K_M` and `qwen3:8b`. The upstream [Qwen2.5-3B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) identifies `qwen-research`, while [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) identifies Apache-2.0 (checked 19 October 2026). Do not describe all Qwen models as Apache-licensed. These upstream pages do not attest the exact historical quantized artifact used in the capture. The repository license does not replace model terms; this note does not assert that model-weight terms automatically apply to generated responses. Establishing the historical artifact's provenance and any applicable publication conditions remains a separate task. Existing capture and failure evidence remain unchanged.

### Still present; bounded improvement

The local JSON file reader checks size before reading. A concurrently growing file could exceed that earlier check. A bounded read would close this local-file race; it is not fixed by the model-response grading change.

The 18 measured responses on nine authored tasks remain a bounded reference case, not a representative benchmark or a deployment recommendation. No new model or measurement was added.
