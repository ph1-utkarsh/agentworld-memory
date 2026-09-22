"""Unseen-template memory experiment with exact ground truth and fixed slots."""
import argparse, hashlib, io, json
from pathlib import Path
import numpy as np
from memory import Consolidated,Episodic,First,Null,Reservoir,Salience,Sliding,answer,grade
from world import generate,manifest,observe,render,vision_truth

ROOT=Path(__file__).resolve().parents[1]

def ci(values,seed=0):
    rng=np.random.default_rng(seed); x=np.asarray(values,float)
    means=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(2000)])
    return [float(np.percentile(means,2.5)),float(np.percentile(means,97.5))]

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--run-id",required=True); args=parser.parse_args()
    out=ROOT/"agentworld/experiments"/args.run_id; out.mkdir(parents=True,exist_ok=False)
    rows=[]; world_records=[]
    for horizon in (20,40,80):
      for seed in range(100,150):
        world=generate(seed,horizon,"passive"); data,digest=manifest(world)
        image=render(world); buffer=io.BytesIO(); image.save(buffer,format="PNG")
        visual=grade(vision_truth(image),world["truth"])
        world_records.append({"seed":seed,"horizon":horizon,"manifest_sha256":digest,"image_sha256":hashlib.sha256(buffer.getvalue()).hexdigest(),"vision_score":visual["score"]})
        for budget in (2,4):
          policies=(("null",Null(budget)),("first",First(budget)),("reservoir",Reservoir(budget)),
                    ("sliding",Sliding(budget)),("salience",Salience(budget)),
                    ("episodic",Consolidated(budget)))
          for name,policy in policies:
            for event in world["events"]: policy.add(observe(event,"passive"))
            result=grade(answer(policy,world["entities"]),world["truth"])
            rows.append({"seed":seed,"horizon":horizon,"budget":budget,"policy":name,**result})
    aggregates=[]
    for horizon in (20,40,80):
      for budget in (2,4):
        item={}
        for name in ("null","first","reservoir","sliding","salience","episodic"):
          values=[r["score"] for r in rows if r["horizon"]==horizon and r["budget"]==budget and r["policy"]==name]
          item[name]={"mean":float(np.mean(values)),"bootstrap_95":ci(values,horizon+budget)}
        base=item["sliding"]["mean"]; item.update(horizon=horizon,budget=budget,
          relative_gain_percent=float(100*(item["episodic"]["mean"]-base)/base) if base else None)
        aggregates.append(item)
    config={"train_templates":["direct"],"test_template":"passive","test_seeds":[100,149],"horizons":[20,40,80],
            "budgets":[2,4],"bootstrap_samples":2000,"paid_spend":0,"model_calls":0,
            "interpretation":"exact parser isolates retention; not an LLM or vision evaluation"}
    (out/"config.json").write_text(json.dumps(config,indent=2)); (out/"worlds.json").write_text(json.dumps(world_records,indent=2))
    (out/"rows.json").write_text(json.dumps(rows,indent=2)); metrics={"aggregates":aggregates,
        "image_decode_mean":float(np.mean([r["vision_score"] for r in world_records])),
        "unsupported_total":sum(r["unsupported"] for r in rows),"paid_spend":0}
    (out/"metrics.json").write_text(json.dumps(metrics,indent=2)); (out/"experiment.py").write_bytes(Path(__file__).read_bytes())
    print(json.dumps(metrics,indent=2))

if __name__=="__main__": main()
