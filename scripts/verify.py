"""Validate the headline AgentWorld evidence without rerunning experiments."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
metrics = json.loads((ROOT / "agentworld/experiments/EXP-AW-006/metrics.json").read_text())
assert metrics["attempt1_mean"] == metrics["reflection_same_evidence_mean"] == 0.25
assert metrics["attempt2_failure_memory_mean"] == 1.0
assert metrics["clean_vision_mean"] == 1.0
assert metrics["adversarial_vision_mean"] == 0.2475
assert metrics["curriculum_generated_worlds"] == 100
assert metrics["paid_spend"] == 0
print("AGENTWORLD VERIFY: PASS")
