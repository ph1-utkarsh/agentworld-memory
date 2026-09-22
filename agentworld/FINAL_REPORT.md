# AgentWorld bounded local report

AgentWorld defines a seeded warehouse schema with time, events, distractors, hidden final truth, two language templates, generated raster observations, exact parsing, temporal/provenance grading, and six slot-budgeted memory policies.

Across 50 unseen seeds, an unseen passive wording template, horizons 20/40/80, and budgets 2/4, entity-consolidated episodic memory beat sliding memory by **63–100% relative** with zero unsupported outputs. Bootstrap intervals and all policy/world rows are preserved. EXP-AW-003 additionally recovers state from raster pixels without symbolic access at 100% exact accuracy.

The result is deliberately narrow: the exact parser, color decoder, and entity-keyed memory align with the generator; no learned vision-language model is evaluated and importance is not learned. It demonstrates controlled multimodal grounding and retention mechanics, not general multimodal continual intelligence.

The named-baseline/repeated-attempt study adds full context, sliding window, vector retrieval, summaries, episodic and hierarchical memory. At horizon 80 with four retrieval slots, sliding scores .5575 and the other five score 1.0; full/vector storage is not budget-matched and is reported separately. Re-running the same evidence (“reflection”) leaves score at .25, whereas extracting missed-entity experiences improves the next attempt to 1.0. One hundred failure-triggered horizon-120 curriculum worlds leave sliding at .25. Replacing true image markers with false same-color evidence reduces raster grounding from 1.0 to .2475.
