from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    minMeta = sugarscape.GetHyperParameter("min_metabolism")
    maxMeta = sugarscape.GetHyperParameter("max_metabolism")
    
    # If already set (from being born), don't reset
    if agent.GetProperty("sugar_metabolism") == None:
        agent.SetProperty("sugar_metabolism", random.randint(minMeta, maxMeta))
        agent.SetProperty("spice_metabolism", random.randint(minMeta, maxMeta))

    #endowment
    min, max = sugarscape.GetHyperParameter("initial_endowment_range")
    if agent.GetProperty("sugar_wealth") == None:
        agent.SetProperty("sugar_wealth", random.randint(min, max))
    
    if agent.GetProperty("spice_wealth") == None:
        agent.SetProperty("spice_wealth", random.randint(min, max))

def SugarStep(sugarscape: Sugarscape, agent: Agent):
    DoSugarStep(sugarscape, agent)

def SugarAndSpiceStep(sugarscape: Sugarscape, agent: Agent):

    alive = True
    
    if alive:
        alive = DoSpiceStep(sugarscape, agent)

    if alive:
        alive = DoSugarStep(sugarscape, agent)

def DoSpiceStep(sugarscape: Sugarscape, agent: Agent) -> bool:
    # Collect sugar at position
    spiceValue = sugarscape.GetScape("spice").GetValue(agent.x, agent.y)
    agent.SetProperty("spice_gathered", spiceValue)
    
    # Remove all sugar at site
    sugarscape.GetScape("spice").SetDefault(agent.x, agent.y)
    currentSpiceWealth = agent.GetProperty("spice_wealth")
    spiceMetabolicRate = agent.GetProperty("spice_metabolism")
    finalSpiceValue = currentSpiceWealth + spiceValue - spiceMetabolicRate
    agent.SetProperty("spice_consumed", spiceValue - spiceMetabolicRate)
    finalSpiceValue = max(finalSpiceValue, 0)
    agent.SetProperty("spice_wealth", finalSpiceValue)
    
    # if spice is 0, we are dead
    if finalSpiceValue == 0:
        sugarscape.KillAgent(agent, "spice_death")
        return False
    return True

def DoSugarStep(sugarscape: Sugarscape, agent: Agent) -> bool:
    # Collect sugar at position
    sugarValue = sugarscape.GetScape("sugar").GetValue(agent.x, agent.y)
    agent.SetProperty("sugar_gathered", sugarValue)
    
    # Remove all sugar at site
    sugarscape.GetScape("sugar").SetDefault(agent.x, agent.y)
    currentSugarWealth = agent.GetProperty("sugar_wealth")
    sugarMetabolicRate = agent.GetProperty("sugar_metabolism")
    finalSugarValue = currentSugarWealth + sugarValue - sugarMetabolicRate
    agent.SetProperty("sugar_consumed", sugarValue - sugarMetabolicRate)
    finalSugarValue = max(finalSugarValue, 0)
    agent.SetProperty("sugar_wealth", finalSugarValue)
    
    # if sugar is 0, we are dead
    if finalSugarValue == 0:
        sugarscape.KillAgent(agent, "sugar_death")
        return False
    return True