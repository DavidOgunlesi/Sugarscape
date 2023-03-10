from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    minMeta = sugarscape.GetHyperParameter("min_metabolism")
    maxMeta = sugarscape.GetHyperParameter("max_metabolism")
    
    # If already set (from being born), don't reset
    if agent.GetProperty("metabolism") == None:
        agent.SetProperty("metabolism", random.randint(minMeta, maxMeta))
        agent.SetProperty("spice_metabolism", random.randint(minMeta, maxMeta))
        
    #endowment
    min, max = sugarscape.GetHyperParameter("initial_endowment_range")
    if agent.GetProperty("sugar_wealth") == None:
        agent.SetProperty("sugar_wealth", random.randint(min, max))
    
    if agent.GetProperty("spice_wealth") == None:
        agent.SetProperty("spice_wealth", random.randint(min, max))

def Step(sugarscape: Sugarscape, agent: Agent):
    # Collect sugar at position
    sugarValue = sugarscape.GetScape("sugar").GetValue(agent.x, agent.y)
    agent.SetProperty("sugar_gathered", sugarValue)
    
    # Remove all sugar at site
    sugarscape.GetScape("sugar").SetDefault(agent.x, agent.y)
    currentSugarWealth = agent.GetProperty("sugar_wealth")
    metabolicRate = agent.GetProperty("metabolism")
    finalValue = currentSugarWealth + sugarValue - metabolicRate
    agent.SetProperty("sugar_consumed", sugarValue - metabolicRate)
    finalValue = max(finalValue, 0)
    agent.SetProperty("sugar_wealth", finalValue)
    
    # if sugar is 0, we are dead
    if finalValue == 0:
        sugarscape.KillAgent(agent)
         