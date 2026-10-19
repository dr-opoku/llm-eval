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

The [artifact provenance follow-up dated 19 October](../evidence/local-smoke-2026-10-15/PROVENANCE.md) records recovered historical model-file references and license texts, matching manifest identifiers in an August inventory, and full-file hash verification of the current local artifacts. The original collection contains this evidence; the reduced public export omits those metadata fields. The earlier description of the capture as containing only model tags was therefore incomplete.

For this capture and future additions:

1. Distinguish model tags, manifest digests, quantized-file digests and upstream revisions. The follow-up identifies the first three for this capture. Exact upstream revision and complete quantization lineage remain unestablished.
2. Record which license text accompanied each artifact. The recovered text for Qwen2.5-3B is the Qwen Research license; the text for Qwen3-8B is Apache-2.0. The follow-up provides their SHA-256 identifiers and upstream references. Do not describe all Qwen models as Apache-licensed.
3. Keep evaluator licensing separate from model licensing. The author chooses the license for the author-owned evaluation software; that choice does not depend on commercial licensing of example models and does not grant model-use rights. New live collection must follow the applicable model terms. Offline report replay does not invoke those models, and this repository distributes no weights.
4. Describe the actual purpose and evidence limits. The collector and capture document bounded evaluation for the reference example. Matching historical references and current hashes identify the declared artifacts; they are not independent attestation of the bytes loaded during inference. Original download details also remain unestablished. A Hugging Face license reference is not a weight download receipt.
5. Preserve every original response and failure. Keep reconstruction in a separate dated note; do not substitute new model identities or present newly collected responses as historical evidence. Check report/data rights separately from model-weight redistribution conditions.

No additional model download, inference or new score is required for this provenance supplement. Missing historical details remain explicitly unestablished, without treating them as missing proof of the author's right to choose the evaluator's license.
