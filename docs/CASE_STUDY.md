# Case study: a bounded configuration assessment

A fictional purchasing desk needs structured supplier-note triage. The task includes extraction, insufficient/conflicting information and untrusted authority claims. `accept` is a triage label, **not** an order or payment approval.

## First, understand the constructed demonstration

The [saved comparison](../examples/comparison.txt) uses three invented configurations, answer-key-derived responses and illustrative durations/costs. It demonstrates that a fluent answer can meet the overall acceptance percentage while failing a mandatory boundary case. The [incomplete example](../examples/incomplete.txt) demonstrates why one accepted response cannot establish eligibility.

Nine authored cases repeated three times are **nine distinct cases and 27 attempt cells**, not 27 independent tasks. There is no independent holdout or production observation.

## Then, inspect one genuine local smoke run

On 15 October 2026, the unchanged pre-review runner collected new responses from two already installed Ollama configurations. No models were downloaded for that capture. The original nine public authored cases and original policy were frozen before collection: ≥85% acceptance, all boundary cells accepted, nine distinct cases and full-request p95 ≤3.0 seconds. **No cost ceiling was required.**

| Configuration label | Accepted / attempts | Boundary cells failing a requirement | Full-request p95 | Sample outcome |
| --- | --- | --- | --- | --- |
| `qwen2.5:3b-instruct-q4_K_M` | 2/9 | 3 | About 9.01 s | Does not meet sample rules |
| `qwen3:8b` | 8/9 | 0 | About 20.79 s | Does not meet sample rules |

The second configuration meets the example's acceptance and boundary requirements but fails the declared latency ceiling. This is a concrete example of separating a promising answer sample from an operating requirement. The policy was not relaxed after observing results.

Inspect the [capture and conditions](../evidence/local-smoke-2026-10-15/README.md), [complete run](../evidence/local-smoke-2026-10-15/run.json), [frozen benchmark](../evidence/local-smoke-2026-10-15/benchmark.json), [report text](../evidence/local-smoke-2026-10-15/report.txt) and [report JSON](../evidence/local-smoke-2026-10-15/report.json). Download/open the [HTML report](../evidence/local-smoke-2026-10-15/report.html) locally.

No execution error occurred; every task response is retained, including answers that fail grading. Costs and human work time were not measured. Model tags are recorded but weight identity was not independently verified. There was one attempt per case, fixed configuration order, no randomized crossover, no held-out tasks and no controlled hardware/load study. These results cannot support a general comparison of the model families or vendors, a production purchasing recommendation or a statistical performance claim.

A failed boundary requirement can mean wrong formatting or content as well as the proposed decision; inspect the per-attempt reason codes. The evaluator does not execute tools or test real access control. The truth of the free-form reason is not graded.

## Why this is relevant to scoped transformation work

The reference demonstrates defining a decision, freezing requirements, instrumenting attempts, preserving inconvenient observations and communicating what remains unresolved. A business owner, technical lead and procurement/risk stakeholders can inspect the same evidence. Organizational adoption, enterprise delivery and financial benefit need separate project evidence.

For a real assignment, use the [independent evaluation protocol](EVALUATION_PROTOCOL.md) before collecting the decision sample. A capable model can recreate this small codebase; this reference makes no claim that software complexity itself establishes a defensible product or willingness to pay.

## Replay without model calls

```bash
python3 -m llm_eval evaluate evidence/local-smoke-2026-10-15/run.json \
  --benchmark evidence/local-smoke-2026-10-15/benchmark.json
python3 scripts/reproduce_examples.py --check
python3 -m unittest discover -s tests -v
```

## Completed decision narrative

The [decision brief](DECISION_BRIEF.md) brings the existing measured capture to a concise conclusion without adding models, changing requirements or replacing failed responses. It records the decision consequence, proposed stakeholder responsibilities and evidence limits.
