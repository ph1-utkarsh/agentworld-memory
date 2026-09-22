# Project State

- Objective: measure bounded continual memory in procedurally generated multimodal worlds.
- Status: ACTIVE under user's 2026-09-21 completion directive.
- Architecture/world domains: intentionally undefined.
- Domain: procedurally generated warehouse object-tracking with symbolic events and deterministic raster observations.
- Budget/model: zero paid calls; primary memory experiment is model-free with exact ground truth to isolate memory policy.
- Multimodal policy: generated raster assets only; no claim that text-only Qwen has vision.
- Implemented: formal events/truth schema, seeded generator, passive/direct template split, deterministic raster renderer, exact temporal/provenance parser and grader, and six bounded memory policies.
- Evidence: EXP-AW-002 evaluates 50 unseen seeds across horizons 20/40/80 and budgets 2/4. Entity-consolidated episodic memory improves exact final-state score 63–100% relative to sliding with zero unsupported outputs.
- Limitation: the parser and entity-keyed memory align strongly with the generated schema; this supports the bounded mechanism, not general multimodal-agent capability.
- Raster grounding: EXP-AW-003 decodes generated images without symbolic-state access at 100% exact recovery. This is deterministic color grounding, not VLM evidence.
- EXP-AW-006 covers the six named baselines. At horizon 80/budget 4, sliding scores .5575 while full context, vector retrieval, summaries, episodic and hierarchical policies score 1.0. Same-evidence reflection leaves .25 unchanged; failure-derived memory raises retry score to 1.0.
- Failure-triggered curriculum generated 100 horizon-120 worlds; sliding remains .25. Adversarial false-color evidence reduces raster grounding from 1.0 to .2475.
