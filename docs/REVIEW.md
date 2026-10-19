# Showcase stress review — 15 October 2026

**Status update — 19 October 2026:** this document records the earlier review. The owner-selected license is now included as [LICENSE.md](../LICENSE.md); earlier licensing remarks describe the historical review scope. See [current findings and corrections](PUBLICATION_STATUS.md) and [usage guidance](PROJECT_STATUS.md).

## Purpose and sequence

Improve visible usefulness, first-run clarity, evidence discipline and professional reference value. The existing source was inspected, baseline tests and adversarial probes were recorded, and the proposed plan was externally reviewed **before repository changes**. The baseline commit was `876d1c15be2c8bcd63ae44c05b53b540f4cb08fe`.

One AGY review per repository was requested with **`gemini-3.8-flash-high`**, the adapter's Gemini 3.8 Flash (High) selector. The three repositories were mounted read-only for the reviewer. File hashes remained unchanged at the pre-edit gate. This records the requested selector; backend model identity was not independently attested.

The reviewer assessed a curated plan/source packet, not every helper or fixture, and did not execute tests. Its recommendations were checked against actual code. This was not a second comprehensive security audit, a market validation or a CV verification. Full local review records are kept outside the repositories; the implementation decisions follow below.

## Accepted findings and repairs

- Protect bundled benchmark, explicit inputs and save-run/report paths from collisions.
- Handle huge numeric values without an uncaught OverflowError.
- Reject an impossible distinct-case minimum greater than benchmark size.
- Complete cost observations with zero accepted responses fail a required cost gate; the undefined ratio stays null.
- Explain that unknown local costs prevent eligibility only if a cost ceiling is required; never relax the frozen policy after observing outcomes.
- Add offline tests, defensive consumer, frozen future evaluation protocol and a bounded measured smoke capture.

## Findings bounded or rejected after source inspection

- The reviewer example demo --benchmark is not a valid CLI invocation; the bundled-fixture collision is nevertheless reproduced separately.
- Do not add tests before the pre-edit gate; baseline absence of a suite and adversarial probes were recorded first.
- No MCP adapter/job for llm-eval; it has no MCP interface.
- Do not replace retained failed attempts with an early silent abort or successful retries.
- The supplied benchmark actually sets maximum_cost_per_accepted_eur to null. The review claim that default local runs necessarily lack cost-required evidence is incorrect. Retain the original pre-collection policy (p95 <= 3.0 seconds; no required cost ceiling).

## International examples informing presentation

- [Oracle](https://github.com/steipete/oracle): make the first useful command and a local preview legible.
- [Evidently](https://github.com/evidentlyai/evidently): connect a small example with inspectable reports and tests.
- [Promptfoo](https://github.com/promptfoo/promptfoo): keep configurations, evaluation and repeatable checks visible.
- [AGENTS.md](https://agents.md/): provide concise repository instructions for coding agents.

These references informed the entry point, examples and verification. They do not establish a universal showcase standard, explain why a specific repository receives stars or prove demand for this code.

## Professional relevance

The reference can support a conversation about specifying a decision, defining evidence, coordinating correction/acceptance and making limits inspectable by technical and business stakeholders. It does not establish enterprise rollout experience, organizational adoption, savings or proprietary platform capability. Those claims need separate project evidence. No private platform implementation is required or included.

## Python-version regression found by GitHub CI

The first Python 3.11 CI replay exposed different floating-point aggregates from Python 3.12. A focused regression test reproduced the failure before the repair. Explicit `math.fsum` accumulation now reproduces the stored examples on both locally available versions. Original responses, frozen requirements and sample eligibility outcomes were preserved. Overflowing aggregate costs yield a structured input error rather than Infinity.

## Verification and remaining decisions

See [verification results](VERIFICATION.json), [the action plan](ACTION_PLAN.json) and [project status](PROJECT_STATUS.md). Automated tests and saved-report replay check the implementation and its declared examples. They cannot establish label truth, representative sampling, model authenticity or deployment suitability.

At the time of this review, licensing, contribution rights, visibility and release were owner decisions. The license has since been supplied; current permissions and remaining policy choices are recorded in [project status](PROJECT_STATUS.md).

## Follow-up on the truncated ending — 15 October 2026

The original response ended inside its final `limits_of_review` section and was not complete valid JSON. The original raw response has been preserved outside the repository.

A follow-up resumed **the same AGY conversation** with the same requested model selector. Its complete, valid JSON response explicitly identified itself as a **newly formulated continuation**, not a verbatim recovery of the original missing wording. All showcase directories were mounted read-only; the repository remained unchanged during the follow-up. This was a continuation of the original source-packet review, not a second stress test or a review of the implemented changes.

The reviewer supplied these final limits:

- This earlier reviewer did not select or evaluate a license; its review is not an assessment of the subsequently supplied license.
- The review used static analysis of the supplied plan, documentation and source packet. The reviewer ran no commands or tests and consulted no network resources.
- `llm_eval/report.py` and `llm_eval/fixtures/benchmark.json` were outside the supplied packet; their internal implementations were not directly inspected by that reviewer.
- Live Ollama behavior, model weights and host conditions were not observed. Runner findings were based on static analysis.

The continuation returned no additional findings and stated that no substantive findings, blockers or plan changes had been omitted. That statement is the reviewer's account, not independent proof of the inaccessible original ending. The supplied limits are consistent with the review scope already recorded above. No code change or implementation-plan change follows from this continuation; that continuation did not assess licensing; current license status is recorded separately.

## Reference-case closure stress check — 15 October 2026

Before this documentation-only finalization, baseline tests passed, tracked hashes matched the baseline commit and offline re-evaluation exactly matched the stored measured report. Checks confirmed 2/9 and 8/9 accepted attempts, 3 and 0 failing boundary cells, unchanged 3.0-second p95 policy, no candidate and unmeasured costs. The earlier AGY review and completed continuation above are not presented as a new review of this brief.

The [decision brief](DECISION_BRIEF.md) adds only presentation and a bounded conclusion. Raw capture, benchmark, implementation and all failures remain byte-identical. Separate staged models and the operational single-prompt check are excluded. Completion means a closed illustrative decision narrative, not model-market coverage, enterprise validation or a license grant.
