from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    visionVectors = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    
    # Needs to be shuffled to prevent bias
    random.shuffle(visionVectors)
    
    # Look  out as far as vision allows and ignore sites with members of my own tribe
    for i in range(1, agent.GetProperty("vision")+1):
        for v in visionVectors:
            x = agent.x + (v[0] * i)
            y = agent.y + (v[1] * i)
            
            if not agent.scape.IsInBounds(x, y):
                continue
            
            # Ignore all sites
            

def Step(sugarscape: Sugarscape, agent: Agent):
    pass
         