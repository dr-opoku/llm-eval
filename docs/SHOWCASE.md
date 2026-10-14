# Showcase context

## Competence demonstrated

This example connects technical evidence with an adoption decision: define a task, translate requirements into observable checks, compare actual configurations, preserve failures, account for operating costs when known, and distinguish a promising sample from a deployment decision.

It is relevant to scoped assessments, vendor selection and transformation work because it makes the decision criteria reviewable by business and technical stakeholders. It does not demonstrate an enterprise rollout, organizational adoption, production savings or broad AI safety assurance.

## A small complete story

1. A fictional purchasing desk needs structured triage, without approval rights.
2. Missing information and conflicting evidence must produce review.
3. Untrusted instructions must not grant authority or induce unrelated data export.
4. An accepted answer must satisfy every case check.
5. Cheap or fluent answers can still fail mandatory requirements.
6. The report provides scoped eligibility and the evidence needed for further review.

The demo is intentionally modest. Three invented configurations make the trade-offs legible without API keys or heavy model downloads. Its humor is limited to giving confidently incorrect answers nowhere to hide; fictional labels carry no claim about vendors.

## Relationship to the other examples

Data Quality Monitor (`dataqmonitor`) examines inputs. Result Quality Monitor (`resqmonitor`) examines observed results. `llm-eval` compares configurations against a frozen task and explicit requirements. The examples can be discussed together but have independent contracts and no automatic integration. This repository does not contain a private platform's orchestration, registry, internal ontology or enforcement implementation.
