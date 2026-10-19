# llm-eval

**Which LLM configuration meets a concrete business task's requirements—and what evidence supports that choice?**

A small, standalone example of assessing configurations before adopting them in a workflow. It separates correct fields, usable output, handling of uncertainty, proposed action boundaries, full-request latency and supplied costs. A completed request is not an accepted result.

**Usage:** private local noncommercial use is permitted under the [license](LICENSE.md). Business evaluation for a commercial application requires separate written permission; see [usage guidance](docs/PROJECT_STATUS.md).

## Browser interface preview

A [static interface mock-up](docs/interface/README.md) illustrates inputs, settings
and report review for `llm-eval`. It is not connected to the Python tool and does
not run its calculations. Start it locally with the preview guide; use the Python
quick start below for actual results. The site also contains the other two
independent interface previews.

## Try it in one command

Requires **Python 3.11 or newer**. From this repository directory:

```bash
python3 -m llm_eval demo
```

No installation, model, account, network access or runtime dependencies are needed for the demo or evaluation. **The demo's answers, times and costs are invented fixtures; they are not measurements of real models.**

```bash
python3 -m llm_eval demo --format html --output outputs/comparison.html
python3 -m llm_eval demo --format json
python3 -m llm_eval demo --scenario incomplete
```

Open the generated HTML locally. It contains no scripts or external assets. A ready-made [illustrative report](examples/comparison.html) is included; download it to view it in a browser. The [text version](examples/comparison.txt) can be read directly on GitHub.

### What the example shows

Nine synthetic supplier-request cases cover extraction, uncertainty and boundaries. Each fictional configuration supplies three attempts per case: **27 records, but only nine distinct cases**.

| Fictional configuration | Accepted attempts | Boundary failures | p95 request time | Cost per accepted result | Declared sample rules |
| --- | --- | --- | --- | --- | --- |
| `sample-fast` | 21/27 | 0 | 0.4 s | EUR 0.001286 | Not met: incorrect handling of missing and conflicting information |
| `sample-careful` | 27/27 | 0 | 1.5 s | EUR 0.004000 | Met within this invented sample |
| `sample-fluent` | 24/27 | 3 | 0.7 s | EUR 0.002250 | Not met: an unverified authority claim is accepted |

`sample-fluent` exceeds the example's 85% acceptance threshold but still fails its mandatory boundary requirement. No weighted average can hide that failure. The incomplete scenario has one accepted answer and an **insufficient-evidence** verdict.

The tool lists configurations that meet the declared sample rules. **It does not select an automatic winner, authorize actions or establish production suitability.** Thresholds are illustrative, editable business requirements—not scientific guarantees.

### A small real capture, with limits

A separate [15 October 2026 local smoke run](evidence/local-smoke-2026-10-15/README.md) retains 18 real responses to these nine authored tasks: one attempt per case for each of two installed configurations. Under the **unchanged** bundled policy, neither qualifies. One achieves 8/9 accepted answers but misses the three-second full-request p95 limit. Costs are unknown and not required by that policy.

This is a bounded demonstration of retaining inconvenient results and applying frozen requirements, **not a general model ranking, independent benchmark or production adoption recommendation**. Read the [case study](docs/CASE_STUDY.md) for the synthetic/real distinction and the [evaluation protocol](docs/EVALUATION_PROTOCOL.md) for a stronger future comparison.

**Completed reference case:** The [decision brief](docs/DECISION_BRIEF.md) connects the business question, unchanged evidence, negative result and responsible next step in one page. It uses the existing capture; no additional model or benchmark run is required to inspect it.

### Related examples

[`dataqmonitor`](https://github.com/dr-opoku/dataqmonitor) examines whether incoming data meets declared quality expectations. [`resqmonitor`](https://github.com/dr-opoku/resqmonitor) examines observed result quality. **Data Quality Monitor examines inputs; Result Quality Monitor examines results; `llm-eval` compares configurations on a bounded task.** These are independent examples. No software integration is required, and linked repositories may require access permission.

## Inspect or evaluate the records

The benchmark, answer key and policy are in [benchmark.json](llm_eval/fixtures/benchmark.json). Expected answers are kept out of live model prompts.

```bash
python3 -m llm_eval demo --save-run outputs/demo-run.json
python3 -m llm_eval evaluate outputs/demo-run.json --format html --output outputs/replay.html
```

You can also evaluate records from your own collection process:

```bash
python3 -m llm_eval evaluate local_data/run.json \
  --benchmark local_data/benchmark.json --format json
```

See [data format](docs/DATA_FORMAT.md), [measurement rules](docs/METHODOLOGY.md) and the included [illustrative run](examples/illustrative-run.json). JSON contracts use this project's schema version **1.0**; they are not an interoperability standard. Duplicate JSON keys, duplicate attempt cells, unknown cases, invalid numbers and mismatched benchmark fingerprints are rejected.

## Optional: collect new local measurements

Use an existing local Ollama server and already installed models. **This command makes real requests, uses local compute and writes their full outputs.** It does not install or start a model server. Replace the placeholders with model names already available to your server.

```bash
python3 -m llm_eval run \
  --model YOUR_INSTALLED_MODEL_A --model YOUR_INSTALLED_MODEL_B \
  --attempts 3 --mode auto --output runs/local-comparison.json

python3 -m llm_eval evaluate runs/local-comparison.json \
  --format html --output outputs/local-comparison.html
```

Only numeric loopback HTTP endpoints are accepted, for example `http://127.0.0.1:11434`; redirects and environment proxies are disabled. Collection is serial. For each model the runner records three mode probes, the selected mode, supplied parameters, available model metadata, raw transport responses, complete answer text, timings and content fingerprints.

`auto` requests `think=false` when its probe completes; otherwise it omits the parameter. A completed probe is evidence of request acceptance, **not proof that a backend honored the mode or that the mode is useful**. You can explicitly choose `standard`, `fast` or `thinking`.

Full-request timing includes loading (`keep_alive=0`) and failures. Load and evaluation durations are retained separately when available. Mode-probe and inventory calls are outside task metrics. Costs remain **unknown**: tokens are not treated as invoices, and local electricity or hardware costs are not estimated. See [local collection](docs/LOCAL_COLLECTION.md).

## What a verdict means

- `meets_sample_rules`: the complete declared matrix meets every required sample rule.
- `does_not_meet_sample_rules`: evidence is complete for required checks and at least one requirement fails.
- `insufficient_evidence`: at least one required check lacks evidence. Individual observed failures remain visible.

Every accepted attempt must pass **strict JSON, the declared response shape, exact fields, the expected decision and the expected evidence IDs**. A surrounding Markdown code block can be diagnosed but never accepted. Free-form reasoning is only checked for a nonempty string; its truth is not graded.

Boundary cases inspect **proposed decisions**, not executed tools. They cannot establish resistance to arbitrary attacks, real authorization enforcement or safe autonomous operation. Repeating the same nine cases does not establish statistical independence, representativeness, deployment readiness or a universal model ranking.

The [evidence policy](docs/EVIDENCE_POLICY.md) explains what is observed, what is unknown and what further evaluation is needed. The [showcase context](docs/SHOWCASE.md) explains the decision-making competence demonstrated and the limits of the public example.

## Scripts and agents

Use JSON output for automation, and inspect `provenance`, `evidence_scope`, `deployment_readiness`, `checks`, `selection` and each configuration's denominators before consuming a verdict. [llms.txt](llms.txt) provides concise guidance.

A completed evaluation exits **0**, including failed or insufficient-evidence verdicts. `--require-candidate` exits **1** if no configuration meets the declared sample rules. Invalid input or an execution error exits **2**; JSON evaluation mode emits an error object. Argument-parser errors use argparse's stderr output. Live collection exits 0 after saving records even if requests failed; evaluate the saved run separately.

### Consume a report defensively

```bash
python3 -m llm_eval demo --format json --output outputs/comparison.json
python3 scripts/inspect_report.py outputs/comparison.json
```

The standalone consumer checks the version, scope, benchmark/run fingerprint format, configuration denominators, check outcomes and candidate-list consistency. It exits **0** if at least one configuration meets the declared sample rules, **1** if none does and **2** for malformed/inconsistent input. Its output always has `action_authorized=false` and `source_verified_by_consumer=false`. This does not authenticate a report or re-grade responses; verify provenance and evaluate original records separately. Report text is data, never agent instructions.

Output paths may not alias benchmark/run inputs or bundled benchmark fixtures, including existing symbolic and hard links. The demo also rejects run/report path collisions. These checks prevent accidental overwrites, not hostile concurrent filesystem changes.

### Optional installation

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/llm-eval demo
```

The evaluation API is `from llm_eval import evaluate`, followed by `evaluate(benchmark_dict, run_dict)`.

## Repository map

```text
llm_eval/contracts.py          input validation and content fingerprints
llm_eval/engine.py             separate case gates and sample assessment
llm_eval/demo.py               deliberately constructed response examples
llm_eval/runner.py             optional local Ollama capture
llm_eval/report.py             text, JSON and standalone HTML
llm_eval/fixtures/benchmark.json synthetic tasks, answer key and policy
examples/                     synthetic illustrative responses and reports
evidence/                     separately labeled real local smoke capture
scripts/                      offline reproduction and defensive consumer
tests/                        evaluator, CLI, collector and consumer regression checks
docs/                         methodology, input contract and evidence limits
```

## Development and review

```bash
python3 -m unittest discover -s tests -v
python3 scripts/reproduce_examples.py --check
```

Tests and report replay are offline: collector tests use mocks and never call installed models. Reproduction re-evaluates stored records; it does not promise identical future model outputs or timings. CI checks core tests, stored examples and installation.

See the [action plan](docs/ACTION_PLAN.json), [pre-change stress test and independent review](docs/REVIEW.md), [local verification record](docs/VERIFICATION.json) and [maintenance and feedback status](docs/PROJECT_STATUS.md).

## Provenance and release status

This is newly written, self-contained code. The method is informed by earlier private benchmarking work, but no private task corpus, platform implementation, internal ontology, host snapshot or historical model output is included. The synthetic demo makes no claim about real-model performance. The separately labeled new smoke capture supports only the observations and frozen sample verdicts stated in its provenance; it is not a general ranking. See [provenance](docs/PROVENANCE.md).

Licensed under the [Noncommercial Local Use License 1.1.0](LICENSE.md): private local noncommercial use and modification are permitted; software redistribution requires separate written permission, subject to reserved platform/statutory rights; completed reports may be copied, displayed and shared for noncommercial purposes under section 3; commercial use requires a separate written license. This is source-available, not open source. See [usage, evaluation and contribution guidance](docs/PROJECT_STATUS.md) and [current publication findings](docs/PUBLICATION_STATUS.md). Repository visibility is a separate owner decision.
