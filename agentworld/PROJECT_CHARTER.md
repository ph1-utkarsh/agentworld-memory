# AgentWorld Project Charter

## Problem and motivation

Agent memory systems are often evaluated on static question answering or anecdotal demonstrations. We need controllable, long-running multimodal worlds with hidden ground truth to distinguish useful retention, harmful retrieval, reflection effects, and extra-compute effects.

## Research question and hypothesis

**Question:** Under a fixed context and memory budget, which memory policy improves long-horizon performance on unseen procedurally generated worlds, and when does memory hurt?

**Hypothesis:** A budgeted hierarchical episodic memory with learned/validated importance, consolidation, and forgetting will improve unseen-world task score by at least **10% relative** over the strongest token-budget-matched sliding-window, summary, or vector-retrieval baseline at long horizons, without increasing unsupported-evidence rate by more than 2 absolute points.

The hypothesis is falsified if benefits vanish after matching tokens/tool calls, fail on unseen templates/seeds, or increase provenance/temporal errors beyond the threshold.

## Target users

Agent and memory researchers, evaluation researchers, and builders of auditable enterprise-workflow agent testbeds.

## Success criteria

- Formal world schema with state, events, observations, actions, hidden truth, distractors, and time.
- Procedural train/development/test worlds split by both seed and template family.
- Executable outcome/intermediate/provenance/temporal graders plus calibrated judge-disagreement study.
- Six memory baselines compared under equal context, memory, tool, and inference-token budgets.
- Repeated-attempt learning, forgetting, reflection compute control, scaling, and multimodal distractor ablations.
- Reproducible world manifests, trajectories, raw scores, failures, and costs.

## Non-goals

Coding repositories as the primary environment; production browser automation; unrestricted real-world communications; persistent storage of personal data; claiming human-like lifelong learning; weight updates in the primary continual-memory study.

## Constraints

Target eleven weeks after Helix. Prefer generated/licensed artifacts and deterministic ground truth. API/model-judge spend and model access are unapproved. Multimodality must be introduced only after text/table world graders are reliable.

## Risks and kill criteria

Risks include generator shortcuts, invalid diversity, evaluator circularity, memory leakage of ground truth, uncontrolled inference compute, weak multimodal grounding, and scope explosion. Redesign if generated worlds are solvable from artifacts/shortcuts, graders cannot reach pre-registered agreement, memory budgets cannot be fairly normalized, or the claimed method does not beat simple baselines on unseen templates.

## Stage Gate 0 status

`DRAFT/PASS-CONDITIONAL`. Revalidate after ForgeRL/Helix, current landscape research, resource approval, and a concrete world-domain choice. AgentWorld is not active.
