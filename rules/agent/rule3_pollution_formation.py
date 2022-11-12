from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass

def Step(sugarscape: Sugarscape, agent: Agent):
    oldPol = sugarscape.GetScape("pollution").GetValue(agent.x, agent.y)
    gatherPol = 20
    consumptionPol = 20
    newPol = oldPol + gatherPol + consumptionPol
    sugarscape.GetScape("pollution").SetValue(agent.x, agent.y, newPol)
        
        
        
         