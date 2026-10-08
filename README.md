# AgentWorld

[![tests](https://github.com/ph1-utkarsh/agentworld-memory/actions/workflows/tests.yml/badge.svg)](https://github.com/ph1-utkarsh/agentworld-memory/actions/workflows/tests.yml) [![license: MIT](https://img.shields.io/badge/license-MIT-c9ff3d.svg)](LICENSE)

**A procedural multimodal benchmark for measuring memory, failure learning and long-horizon agent behavior.**

AgentWorld generates symbolic and raster warehouse environments with exact graders. Six memory strategies receive the same observations and action budget, making it possible to isolate when memory—not extra evidence—changes an agent’s result.

## Main result

Failure became usable memory.

| Condition | Exact normalized score |
|---|---:|
| First attempt | **0.25** |
| Reflection with the same evidence | **0.25** |
| Second attempt with failure memory | **1.00** |

Reflection alone did nothing. Supplying the missing evidence retained from failure raised the result from **0.25 to 1.00**.

## Additional findings

- Six memory baselines: full context, sliding window, vector retrieval, summaries, episodic and hierarchical memory
- Long-horizon score with a four-item retrieval budget: **0.5575 sliding**, **1.00 structured strategies**
- Clean raster decoding: **1.00**
- Adversarial false-colour condition: **0.2475**
- Failure-triggered curriculum: **100 worlds**, horizon **120**
- Exact graders and deterministic generation across fixed seeds

## Architecture

```text
seed + template
      │
procedural world ──► symbolic observations + raster frame
      │
memory policy ──► bounded retrieval context
      │
agent answer ──► exact grader ──► failure record
                                      │
                                      └──► retry memory + curriculum
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest discover -s agentworld -p 'test*.py' -v
python3 scripts/verify.py
python3 agentworld/experiment.py --run-id EXP-LOCAL
python3 agentworld/continual_experiment.py --run-id EXP-CONTINUAL-LOCAL
```

Run IDs are immutable; choose unused identifiers.

## Evidence map

- `EXP-AW-003`: six memory policies and raster decoding
- `EXP-AW-004`: preserved ineffective distractor experiment
- `EXP-AW-005`: corrected controlled failure-learning intervention
- `EXP-AW-006`: long-horizon baselines, adversarial vision and generated curriculum
- `agentworld/FINAL_REPORT.md`: scoped conclusions and limitations

## Scope

The current agent is an exact controlled policy, not a learned vision-language model. Full-context and vector-storage totals are not memory-budget matched, although retrieval context is. These constraints keep the demonstrated causal comparison narrow and reproducible.

## License

MIT © 2026 Utkarsh Sharma.
