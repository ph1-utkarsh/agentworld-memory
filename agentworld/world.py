"""Deterministic warehouse world with symbolic and raster observations."""
from dataclasses import dataclass
import hashlib, json, random
from PIL import Image, ImageDraw

COLORS={"red":(220,50,47),"blue":(38,139,210),"green":(133,153,0),"yellow":(181,137,0)}
ROOMS=("A","B","C","D")

@dataclass(frozen=True)
class Event:
    time:int; entity:str; room:str; distractor:bool=False

def generate(seed,horizon=40,template="direct"):
    rng=random.Random(seed); entities=tuple(COLORS); state={e:rng.choice(ROOMS) for e in entities}; events=[]
    for time in range(horizon):
        if time%5==4: events.append(Event(time,"noise",rng.choice(ROOMS),True)); continue
        entity=rng.choice(entities); room=rng.choice(ROOMS); state[entity]=room; events.append(Event(time,entity,room))
    return {"seed":seed,"template":template,"entities":entities,"events":events,"truth":state}

def observe(event,template):
    if event.distractor: return f"t={event.time}: forklift telemetry mentioned room {event.room}."
    if template=="direct": return f"t={event.time}: {event.entity} crate moved to room {event.room}."
    if template=="passive": return f"At time {event.time}, room {event.room} received the {event.entity} crate."
    raise ValueError("unknown template")

def render(world,cell=48):
    image=Image.new("RGB",(cell*2,cell*2),(245,245,245)); draw=ImageDraw.Draw(image)
    for index,room in enumerate(ROOMS):
        x=(index%2)*cell; y=(index//2)*cell; draw.rectangle((x,y,x+cell-1,y+cell-1),outline=(0,0,0)); draw.text((x+3,y+3),room,fill=(0,0,0))
        present=[e for e,r in world["truth"].items() if r==room]
        for j,e in enumerate(present): draw.ellipse((x+7+j*9,y+20,x+14+j*9,y+27),fill=COLORS[e])
    return image

def vision_truth(image,cell=48):
    """Decode colored raster markers without symbolic-state access."""
    pixels=image.load(); result={}
    for entity,color in COLORS.items():
        hits=[(x,y) for y in range(image.height) for x in range(image.width) if pixels[x,y]==color]
        if hits:
            x=sum(p[0] for p in hits)/len(hits); y=sum(p[1] for p in hits)/len(hits)
            result[entity]=ROOMS[int(y//cell)*2+int(x//cell)]
    return result

def manifest(world):
    data={"seed":world["seed"],"template":world["template"],"truth":world["truth"],
          "events":[e.__dict__ for e in world["events"]]}
    encoded=json.dumps(data,sort_keys=True,separators=(",",":")).encode(); return data,hashlib.sha256(encoded).hexdigest()
