# Model artifact provenance — follow-up dated 19 October 2026

This note supplements the [15 October capture](README.md). It records a retrospective consistency review of retained local evidence. It does not change the original requests, responses, failures, parameters, frozen policy or reports, and no new model inference was performed for this review.

## Evidence recovered

The original collection retained Ollama model metadata, including content-addressed `FROM` references and complete license text. The published `run.json` intentionally omitted those metadata fields. The original record therefore contains more artifact evidence than the reduced public export alone.

The review established the following:

- A retained inventory dated 9 August records the same manifest identifiers as the current manifest files. Its model-file references and license texts agree with the original 15 October metadata.
- Full-file SHA-256 checks on 19 October match both current weight files to the model-file references captured on 15 October and the corresponding manifest layers.
- SHA-256 checks match the historical license texts to the current license blobs byte for byte. The associated configuration and metadata blobs were also checked against their manifest sizes and digests.
- Every task record, mode probe and explicit configuration parameter in the public export matches the private original. The stored benchmark fingerprint also matches. All 18 task responses remain unchanged.
- The collector and capture document a bounded evaluation of two installed configurations on nine authored synthetic tasks for this professional reference example.

This is a review of retained local evidence, not independent authentication of the source records. Private captures, templates, host inventories and unrelated model metadata are not published here.

## Artifact identifiers

Both artifacts are declared as GGUF with Q4_K_M quantization. A model-file digest identifies the quantized file; a manifest digest identifies the associated manifest, including its configuration and layer references. Neither is an upstream Hugging Face revision identifier.

### `qwen2.5:3b-instruct-q4_K_M`

- Manifest SHA-256: `357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b`
- Model-file SHA-256: `5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6`
- Model-file size: 1,929,903,008 bytes.
- Captured license: Qwen RESEARCH LICENSE AGREEMENT, release 19 September 2024.
- License-text SHA-256: `b5c0e5cf74cf51af1ecbc4af597cfcd13fd9925611838884a681070838a14a50`
- [Upstream license reference](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/LICENSE).

### `qwen3:8b`

- Manifest SHA-256: `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`
- Model-file SHA-256: `a3de86cd1c132c822487ededd47a324c50491393e6565cd14bafa40d0b8e686f`
- Model-file size: 5,225,374,496 bytes.
- Captured license: Apache License 2.0, January 2004.
- License-text SHA-256: `d18a5cc71b84bc4af394a31116bd3932b42241de70c77d2b76d69a314ec8aa12`
- [Upstream license reference](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE).

The historical captured texts establish which terms were recorded with these local artifacts. The upstream pages, checked on 19 October, provide references; a current web page alone cannot identify a historical local artifact or prove its download history.

## Evaluator rights and model rights

The author's evaluation logic, fixtures and report software are licensed under the repository's [Noncommercial Local Use License 1.1.0](../../LICENSE.md). The chosen license for those author-owned components is separate from the licenses of models used to collect example responses. Choosing or separately licensing the evaluation software does not require the example models to have a commercial-use license, and does not grant rights to use those models.

This repository distributes no model weights and its offline evaluation and report replay do not invoke a model. Anyone collecting new responses must separately follow the applicable model terms. Model-weight redistribution conditions should not automatically be treated as conditions on every benchmark report or generated answer. The evaluator's license and its completed report exception do not replace third-party terms.

## Limits of the reconstruction

The matching historical references, manifests and file hashes provide a consistent artifact identity chain. No independent measurement of the weight bytes actually loaded during the historical inference was collected; the available chain relies on the service's recorded metadata. It does not establish an uninterrupted installation history or independently attest execution hardware or backend behavior.

The original download timestamp, a receipt establishing the historical download source, the exact upstream weight revision and the complete conversion/quantization lineage were not established by this review. The local manifests identify an Ollama registry namespace; links to Hugging Face license documents do not by themselves establish where the quantized weights were downloaded. These distinctions do not invalidate the retained responses and do not turn this bounded example into a representative model comparison.

Keep these identifiers and limits alongside the original evidence. A new download or a fresh run would be a new event, not a replacement for missing historical records.
