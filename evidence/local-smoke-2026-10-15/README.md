# Measured responses to synthetic tasks — 15 October 2026

This folder contains an inspected export of **new local requests**, not historical private benchmarking data. The task cases and labels are public authored synthetic material. The measured provenance applies to requests/responses/timings, not to the representativeness or truth of the task labels.

- Collection window: 06:29:19–06:33:48 UTC, 15 October 2026.
- Collector source: baseline `876d1c15be2c8bcd63ae44c05b53b540f4cb08fe`.
- Two installed tags, fixed serial order: `qwen2.5:3b-instruct-q4_K_M`, then `qwen3:8b`.
- Nine cases × one attempt per configuration; 18/18 completed responses, no execution errors or substituted retries.
- Timeout 30 seconds per task, context 4096, output limit 384 tokens, temperature 0, seed 42, `keep_alive=0`, mode auto. Both selected `fast` after the request probe completed; that does not prove the backend honored `think=false`.
- Full client request durations include loading, transfer and client overhead. Available backend load/evaluation durations and raw transport responses are retained.
- Three mode probes per model and inventory calls are outside task metrics. Their records remain visible.
- Costs and human work time are unmeasured. The frozen policy has no required cost ceiling; adding one would require a separately identified evaluation policy.
- The runner reports generic OS/architecture and Ollama version. This export omits model files, templates/system settings, license text and tensor inventory from `model_show`, retaining only details/capabilities. No server inventory or private host snapshot is published.
- Weight digests and hardware execution placement were not independently pinned or verified. Model tags can change. Host activity was not controlled or instrumented continuously, configuration order was not randomized, and repetition/variance were not studied.

[run.json](run.json) preserves every task request, full answer, error field, available timings and fingerprints. `publication_note` discloses the metadata reduction. Fingerprints identify this exported content, not source authenticity. The private original capture is outside the repository; no private task transcripts were used.

[benchmark.json](benchmark.json) preserves the pre-collection policy and answer key. Expected answers were not sent in task requests. [report.json](report.json), [report.txt](report.txt) and [report.html](report.html) are derived offline and checked by `python3 scripts/reproduce_examples.py --check` from the repository root.

This is a collection/evaluation smoke run, **not** an independent held-out benchmark, a model ranking or a deployment recommendation. Neither configuration meets the frozen sample rules, and no policy was adjusted to make either pass.
