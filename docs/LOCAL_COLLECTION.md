# Optional local collection

Only `run` contacts a service. `demo` and `evaluate` make no network requests.

## Prerequisites and execution scope

- Python 3.11 or newer.
- An already running local Ollama server with the selected models already installed.
- Enough memory and time for the chosen models. The program does not download models, start services, change host configuration or execute generated content.

The endpoint must be a numeric loopback HTTP origin (`127.0.0.1` or `::1`). Redirects and environment proxy settings are disabled. This restricts this adapter's destination; it does not establish what a separately configured Ollama backend does internally. Do not supply private prompts unless the server's configuration is appropriate for them.

## Defaults

| Setting | Value |
| --- | --- |
| Attempts per task | 3 |
| Timeout per task request | 120 seconds |
| Mode probe timeout | At most 30 seconds |
| Context requested | 4096 |
| Output token limit requested | 512 |
| Temperature / seed | 0 / 42 |
| Scheduling | Serial |
| Keep alive | 0; full-request timings include loading |

Three modes are probed separately per model: parameter omitted, think=false, think=true. All probe requests and returned raw responses are saved. A failed or timed-out probe does not prove that the mode is unsupported. An accepted parameter does not prove that the runtime honors it. `auto` selects fast when its probe completes; otherwise standard. Explicit modes are sent as requested even if their probe fails; failures remain visible in task records.

The adapter uses the documented [Ollama generate endpoint](https://docs.ollama.com/api/generate), which describes response fields, thinking controls and keep-alive behavior. This small runner probes the omitted/boolean modes only; it does not discover every model-specific thinking level.

The CLI saves an atomic run checkpoint after every task request. Not-yet-run configurations remain present with empty records, so an interrupted run can be evaluated as incomplete. This version does not resume checkpoints; use a new output filename for a new collection. HTTP error bodies are retained within the capture limit; a timeout or network failure may have no recoverable transport body. Model inventory is collected as available metadata, not verified identity.

No schema/JSON generation constraint is injected by the adapter. The instruction asks for JSON, and the actual response is assessed without repair. Thinking tokens or text returned elsewhere in the Ollama response remain in raw transport; only the response field is treated as the answer. Reaching a token limit can produce a failed answer and is part of the configuration being assessed.

## Reproducibility limits

The runner captures available model metadata, server version, OS family, architecture, requested parameters, full responses and available load/evaluation durations. It does not continuously monitor CPU, memory, energy, host load or background activity. Requested context is not proof of the effective context available to the model. A seed is not a cross-model or cross-runtime determinism guarantee.

Record quantization, model digest, runtime version, hardware, host workload and execution dates where available. Evaluate comparable conditions separately; local loading-inclusive times and cloud request times should not be merged into an unexplained speed ranking.

Task costs are null by design. If adding costs, describe the actual source and allocation method, include failed attempts and explicitly state excluded expenses. Do not convert token counts into a claimed bill without the applicable pricing and usage information.

## Handling captured content

Run JSON can contain your custom instructions, inputs, model templates, metadata and entire answers. Store captures under ignored `runs/` or `local_data/`, review their contents before sharing and keep synthetic examples separate from measurements. `.gitignore` helps prevent accidental additions; it is not a secret scanner or access-control mechanism.
