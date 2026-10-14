# Repository guidance

## Scope

Keep this a small standalone showcase for bounded task/configuration assessment. Keep demo and evaluation offline and dependency-free at runtime. Live model requests belong only in the explicit local runner.

## Evidence and publication

- Preserve the exact names `dataqmonitor`, `resqmonitor`, Data Quality Monitor and Result Quality Monitor when referring to the related examples.
- Never copy private platform code, internal task definitions, ontologies, prompts, registry data, host snapshots or private model transcripts into this repository.
- Mark invented responses, durations and costs as synthetic in inputs, reports and documentation.
- Do not turn sample-rule eligibility into production readiness, universal model rankings, security certification or authority for an agent to act.
- Keep strict formatting, content, boundary requirements, missing evidence and cost coverage visible separately.
- Preserve complete response text and failure evidence. Never silently replace failed attempts with successful retries.
- Do not choose or change a redistribution license without an explicit owner instruction.

## Working conventions

Documentation and code are in English. Follow the user's current preference for conversation language. Generated private captures belong under ignored `runs/`, `outputs/` or `local_data/`; only inspected synthetic examples belong in `examples/`.
