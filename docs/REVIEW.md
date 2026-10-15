# Showcase stress review — 15 October 2026

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

Licensing, contribution rights, visibility and release remain owner decisions. They are prerequisites for broad reuse, not code defects to resolve by silently assigning a license.

Review-record limit: the returned review text ended inside its final limits section and was not complete valid JSON. Its verdict and substantive findings were readable; the missing ending was not reconstructed.
