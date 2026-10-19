# Provenance and publication boundary

## What informed the method

Earlier private benchmarking work in April–August 2026 explored local and hosted configurations, empirical mode probes, structured responses, timing, frozen task definitions, full evidence capture and capture-layer errors. These observations informed the design principles used here.

This repository is **newly written** and has its own synthetic supplier-triage task. No earlier private task package, answer key, semantic definition, response transcript, internal host snapshot, registry, platform code or model weights are copied into this repository. It is not an extraction of a private product's core implementation.

## What is included

- Nine newly authored cases and explicit expected answers.
- Fictional configurations with intentionally constructed successes and failures.
- Invented task costs and durations, prominently labeled as synthetic.
- A standalone evaluator, report renderer and optional local collector.

The included illustrative run and reports were generated from those fixtures on 14 October 2026. They demonstrate report construction, not real model performance, benchmark independence or implementation verification. No historical August scores are republished as current vendor claims.

## Separate new real smoke capture

The [local smoke capture dated 15 October 2026](../evidence/local-smoke-2026-10-15/README.md) was newly collected against the unchanged public task and policy. It is separate from the invented demo and earlier private benchmarking. It retains all 18 task responses, probes, request parameters, raw transport, failures and timings available to the collector. The published capture omits model templates, modelfiles, tensor listings and unrelated model metadata; the capture note identifies that reduction.

It is one serial local run with one attempt per case/configuration, no held-out tasks, no independent answer-key review, no controlled host-load experiment, no invoiced cost and no measured human effort. It demonstrates inspection and rule application, not comparative model superiority or a successful organizational deployment. See the capture's provenance for the exact conditions and limits.

## Extending the public example

New real measurements should keep their original task version, run conditions and provenance. A new dataset derived from private work needs a content review before publication. Replacing identifiers alone may leave internal semantics or operating assumptions exposed.

The owner-selected [Noncommercial Local Use License 1.1.0](../LICENSE.md) is included. It covers rights held by the licensor and does not replace third-party terms. Repository visibility is a separate owner decision; see [current publication findings](PUBLICATION_STATUS.md).

## Model artifact and rights checklist

The historical capture records model tags, not independently pinned weight digests. A tag is a mutable label, not proof of a particular quantized artifact or its license. This is a reproducibility and rights-documentation limit, not evidence that the recorded answers are fabricated or that a license violation occurred.

For an additional provenance note, use contemporaneous records if available:

1. Identify the exact artifact using its immutable manifest/weight digest, source, upstream revision and quantization. Record which evidence establishes that it was the artifact used on 15 October; a current installation alone cannot establish that history.
2. Identify applicable upstream and artifact/distributor terms at collection time. The upstream [Qwen2.5-3B-Instruct license](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/LICENSE) grants noncommercial use and calls for a separate license for commercial use; [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) identifies Apache-2.0 (pages checked 19 October 2026). These pages do not independently identify the historical local artifacts.
3. Confirm the original collection purpose and any applicable permissions. This repository is intended as a professional showcase; do not assume the original model use was noncommercial solely because tasks were synthetic or no fee was charged. The definition in each model's own terms controls that model use.
4. Check the intended publication against applicable terms and third-party data rights. The repository contains no weights; do not infer that all weight redistribution conditions automatically apply to a report or that the evaluator's license replaces upstream terms. If a material use was commercial and requires separate upstream permission, resolve that before claiming commercial clearance or undertaking further such use.
5. Preserve the existing capture and failures. Publish a separate dated provenance note identifying verified facts and remaining unknowns; do not rewrite historical responses, substitute a new model identity or present a newly run model as the old capture.

No additional model download, inference or new score is required to explain the existing bounded reference case. Replaying the stored responses with the evaluator does not itself invoke the original models. Missing historical artifact evidence should remain explicitly unknown.
