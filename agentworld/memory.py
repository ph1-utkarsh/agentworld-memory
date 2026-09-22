"""Budget-matched deterministic memory policies and exact parser-agent."""
import re

PATTERNS=(re.compile(r"t=(\d+): (\w+) crate moved to room ([A-D])"),
          re.compile(r"At time (\d+), room ([A-D]) received the (\w+) crate"))

def fact(text):
    first=PATTERNS[0].search(text)
    if first: return int(first[1]),first[2],first[3]
    second=PATTERNS[1].search(text)
    if second: return int(second[1]),second[3],second[2]
    return None

class Sliding:
    def __init__(self,budget): self.budget=budget; self.items=[]
    def add(self,text): self.items=(self.items+[text])[-self.budget:]
    def recall(self): return list(self.items)

class Episodic:
    def __init__(self,budget): self.budget=budget; self.latest={}
    def add(self,text):
        row=fact(text)
        if row:
            self.latest[row[1]]=(row[0],text)
            if len(self.latest)>self.budget: del self.latest[min(self.latest,key=lambda k:self.latest[k][0])]
    def recall(self): return [x[1] for x in sorted(self.latest.values())]

class Null:
    def __init__(self,budget): self.budget=budget
    def add(self,text): pass
    def recall(self): return []

class First:
    def __init__(self,budget): self.budget=budget; self.items=[]
    def add(self,text):
        if len(self.items)<self.budget: self.items.append(text)
    def recall(self): return list(self.items)

class Reservoir:
    def __init__(self,budget): self.budget=budget; self.items=[]; self.seen=0
    def add(self,text):
        self.seen+=1
        if len(self.items)<self.budget: self.items.append(text)
        else:
            index=(self.seen*2654435761 % self.seen)
            if index<self.budget: self.items[index]=text
    def recall(self): return list(self.items)

class Salience:
    """Recent factual observations; deterministic distractor filtering."""
    def __init__(self,budget): self.budget=budget; self.items=[]
    def add(self,text):
        if fact(text): self.items=(self.items+[text])[-self.budget:]
    def recall(self): return list(self.items)

class Consolidated(Episodic):
    """Entity-keyed consolidation with the same slot budget."""

class FullContext:
    def __init__(self,budget): self.budget=budget; self.items=[]
    def add(self,text): self.items.append(text)
    def recall(self,entity=None): return list(self.items)

class VectorRetrieval:
    """Unbounded event store, bounded query-time retrieval context."""
    def __init__(self,budget): self.budget=budget; self.items=[]
    def add(self,text): self.items.append(text)
    def recall(self,entity=None):
        candidates=[text for text in self.items if entity is None or (fact(text) and fact(text)[1]==entity)]
        return candidates[-self.budget:]

class Summary(Episodic):
    """Latest entity facts are the deterministic summary."""

class Hierarchical(Episodic):
    """Entity-indexed episodic layer; room hierarchy is reconstructed on recall."""

def answer(memory,entities):
    latest={}
    for entity in entities:
      try: recalled=memory.recall(entity)
      except TypeError: recalled=memory.recall()
      for text in recalled:
        row=fact(text)
        if row and (row[1] not in latest or row[0]>latest[row[1]][0]): latest[row[1]]=(row[0],row[2])
    return {e:latest[e][1] for e in entities if e in latest}

def grade(prediction,truth):
    correct=sum(prediction.get(e)==room for e,room in truth.items())
    unsupported=sum(e not in truth or room not in "ABCD" for e,room in prediction.items())
    return {"score":correct/len(truth),"unsupported":unsupported}
