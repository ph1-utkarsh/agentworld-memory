"""Named memory baselines, failure learning, reflection control, and distractor ablations."""
import argparse,hashlib,io,json
from pathlib import Path
import numpy as np
from PIL import ImageDraw
from memory import FullContext,Hierarchical,Episodic,Sliding,Summary,VectorRetrieval,answer,grade,fact
from world import COLORS,generate,observe,render,vision_truth

ROOT=Path(__file__).resolve().parents[1]
POLICIES={"full_context":FullContext,"sliding_window":Sliding,"vector_retrieval":VectorRetrieval,
          "summaries":Summary,"episodic_memory":Episodic,"hierarchical_memory":Hierarchical}

def fill(policy,world):
    observations=[observe(event,world["template"]) for event in world["events"]]
    for text in observations: policy.add(text)
    return observations

def learned_retry(world,budget=2):
    first=Sliding(budget); observations=fill(first,world); prediction=answer(first,world["entities"]); before=grade(prediction,world["truth"])["score"]
    missed={e for e,r in world["truth"].items() if prediction.get(e)!=r}; experience=Episodic(max(len(missed),1))
    for text in observations:
        row=fact(text)
        if row and row[1] in missed: experience.add(text)
    combined=FullContext(budget+len(missed))
    for text in first.recall()+experience.recall(): combined.add(text)
    after=grade(answer(combined,world["entities"]),world["truth"])["score"]
    # Reflection with identical evidence is deliberately a no-op compute control.
    reflected=grade(answer(first,world["entities"]),world["truth"])["score"]
    return before,reflected,after

def distract(image):
    result=image.copy(); pixels=result.load()
    # Remove true markers and insert same-color markers in a fixed wrong region.
    for y in range(result.height):
        for x in range(result.width):
            if pixels[x,y] in COLORS.values(): pixels[x,y]=(245,245,245)
    draw=ImageDraw.Draw(result)
    for index,color in enumerate(COLORS.values()): draw.ellipse((60+index*8,12,67+index*8,19),fill=color)
    return result

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--run-id",required=True); args=parser.parse_args()
    out=ROOT/"agentworld/experiments"/args.run_id; out.mkdir(parents=True,exist_ok=False)
    rows=[]
    for seed in range(200,300):
      for horizon in (20,80):
        world=generate(seed,horizon,"passive")
        for budget in (2,4):
          for name,kind in POLICIES.items():
            policy=kind(budget); observations=fill(policy,world); result=grade(answer(policy,world["entities"]),world["truth"])
            rows.append({"seed":seed,"horizon":horizon,"budget":budget,"policy":name,**result,
                         "stored_observations":len(getattr(policy,"items",getattr(policy,"latest",{})))})
        before,reflected,after=learned_retry(world)
        clean=grade(vision_truth(render(world)),world["truth"])["score"]
        adversarial=grade(vision_truth(distract(render(world))),world["truth"])["score"]
        rows.append({"seed":seed,"horizon":horizon,"policy":"failure_learning","attempt1":before,"reflection_same_evidence":reflected,"attempt2":after,
                     "clean_vision":clean,"adversarial_vision":adversarial})
    policy_means={name:float(np.mean([r["score"] for r in rows if r.get("policy")==name and r.get("budget")==4 and r.get("horizon")==80])) for name in POLICIES}
    retries=[r for r in rows if r.get("policy")=="failure_learning" and r["horizon"]==80]
    failed_seeds=[r["seed"] for r in rows if r.get("policy")=="failure_learning" and r["horizon"]==20 and r["attempt1"]<1]
    curriculum=[]
    for seed in failed_seeds:
        harder=generate(seed,120,"passive"); policy=Sliding(2); fill(policy,harder)
        curriculum.append(grade(answer(policy,harder["entities"]),harder["truth"])["score"])
    metrics={"long_horizon_budget4_means":policy_means,"attempt1_mean":float(np.mean([r["attempt1"] for r in retries])),
      "reflection_same_evidence_mean":float(np.mean([r["reflection_same_evidence"] for r in retries])),"attempt2_failure_memory_mean":float(np.mean([r["attempt2"] for r in retries])),
      "clean_vision_mean":float(np.mean([r["clean_vision"] for r in retries])),"adversarial_vision_mean":float(np.mean([r["adversarial_vision"] for r in retries])),
      "curriculum_generated_worlds":len(curriculum),"curriculum_horizon":120,"curriculum_sliding_mean":float(np.mean(curriculum)),
      "paid_spend":0,"interpretation":"exact generated domain; full/vector storage not memory-budget matched, retrieval context is"}
    config={"test_seeds":[200,299],"template":"passive","horizons":[20,80],"budgets":[2,4],"policies":list(POLICIES),"paid_spend":0}
    (out/"config.json").write_text(json.dumps(config,indent=2)); (out/"rows.json").write_text(json.dumps(rows,indent=2)); (out/"metrics.json").write_text(json.dumps(metrics,indent=2)); (out/"continual_experiment.py").write_bytes(Path(__file__).read_bytes())
    print(json.dumps(metrics,indent=2))

if __name__=="__main__": main()
