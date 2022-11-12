from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    minMeta = sugarscape.GetHyperParameter("min_metabolism")
    maxMeta = sugarscape.GetHyperParameter("max_metabolism")
    agent.SetProperty("metabolism", random.randint(minMeta, maxMeta))
    
    #endowment
    agent.SetProperty("sugar_wealth", sugarscape.GetHyperParameter("initial_endowment"))

def Step(sugarscape: Sugarscape, agent: Agent):
    # Collect sugar at position
    sugarValue = sugarscape.GetScape("sugar").GetValue(agent.x, agent.y)
    # Remove all sugar at site
    sugarscape.GetScape("sugar").SetDefault(agent.x, agent.y)
    currentSugarWealth = agent.GetProperty("sugar_wealth")
    metabolicRate = agent.GetProperty("metabolism")
    finalValue = currentSugarWealth + sugarValue - metabolicRate
    finalValue = max(finalValue, 0)
    agent.SetProperty("sugar_wealth", finalValue)
    
    # if sugar is 0, we are dead
    if finalValue == 0:
        sugarscape.KillAgent(agent)
         