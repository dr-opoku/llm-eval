# What the evidence supports

## Observed, compared, and established

The report keeps three levels separate:

1. **Observed:** response text and supplied execution measurements.
2. **Compared:** whether those observations meet the frozen answer key and declared sample rules.
3. **Established:** only the result for those supplied task cells. Production suitability, general intelligence, causal performance differences and safe autonomous execution remain unestablished.

| Example | Observation | Supported statement | Unsupported statement |
| --- | --- | --- | --- |
| Complete correct synthetic configuration | 27/27 authored answers pass | The fixture demonstrates the acceptance calculation | A real model achieves 100% accuracy |
| Incomplete run | One answer passes; 26 declared cells are missing | One observed answer passed; eligibility is unknown | The configuration is reliable |
| High aggregate acceptance with a boundary failure | 24/27 pass; three B03 attempts fail | The sample's mandatory boundary requirement is not met | The model is universally unsafe |
| Text proposes reject | The response matches the expected boundary label | This text-level case passed | A deployed agent cannot execute an unauthorized action |
| Missing cost | Responses exist without complete cost accounting | Cost per accepted result is unknown | Local execution is free or cheaper |

## Portability across business domains

The example's subject is fictional supplier triage. The reusable pattern is to define bounded inputs, observable outputs, reference evidence, forbidden decisions and operating requirements. A support-routing task, document-intake workflow or reconciliation task would need its own schema, cases and independently reviewed answer key. Changing task nouns is insufficient if the required decisions or risk boundaries differ.

This implementation deliberately stays within exact structured outputs. It does not claim to grade arbitrary legal judgments, medical reasoning, open-ended consulting recommendations or complete agent trajectories.

## People and agents need the same limits

An agent consuming the JSON report should inspect provenance and missing evidence before interpreting candidates. `meets_sample_rules` is never approval to make a purchase, access data, execute a tool or deploy a model. Runtime authorization must be enforced outside model text. A client's confident summary cannot strengthen the underlying evidence.

All supplied records are retained in the run object; original response strings are not repaired. The report exposes per-attempt response fingerprints and grading reasons so a reviewer can inspect the original records. This creates an inspectable chain, not cryptographic proof that the collector or source is trustworthy.
