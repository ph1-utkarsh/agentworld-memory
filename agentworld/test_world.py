import unittest
from memory import Episodic,Reservoir,Sliding,answer,grade
from world import generate,manifest,observe,render,vision_truth

class WorldTests(unittest.TestCase):
    def test_determinism(self): self.assertEqual(manifest(generate(3)),manifest(generate(3)))
    def test_render(self):
        world=generate(1); image=render(world)
        self.assertEqual(image.size,(96,96)); self.assertEqual(vision_truth(image),world["truth"])
    def test_episodic_tracks_latest(self):
        world=generate(5,30,"passive"); memory=Episodic(4)
        for event in world["events"]: memory.add(observe(event,"passive"))
        self.assertEqual(grade(answer(memory,world["entities"]),world["truth"])["score"],1)
    def test_budget(self):
        memory=Sliding(3)
        for i in range(10): memory.add(str(i))
        self.assertEqual(len(memory.recall()),3)
        reservoir=Reservoir(3)
        for i in range(20): reservoir.add(str(i))
        self.assertEqual(len(reservoir.recall()),3)

if __name__=="__main__": unittest.main()
