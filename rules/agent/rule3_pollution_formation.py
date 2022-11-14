from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass

def Step(sugarscape: Sugarscape, agent: Agent):
    oldPol = sugarscape.GetScape("pollution").GetValue(agent.x, agent.y)
    gatherPol = agent.GetProperty("sugar_gathered")*sugarscape.GetHyperParameter("pollution_per_sugar")
    consumptionPol = agent.GetProperty("sugar_consumed")*sugarscape.GetHyperParameter("pollution_per_sugar")
    newPol = oldPol + gatherPol + consumptionPol
    sugarscape.GetScape("pollution").SetValue(agent.x, agent.y, newPol)
        
        
        
         