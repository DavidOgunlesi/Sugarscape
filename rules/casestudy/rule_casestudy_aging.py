from typing import List, Tuple, Callable
from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass

def Step(sugarscape: Sugarscape, agent: Agent):
    age = agent.GetProperty("age")
    lifespan = agent.GetProperty("life_span")
    degeneration_start_age = sugarscape.GetHyperParameter("degeneration_start_age")
    ageDegenerationFactor = min(1,max(0, (age-degeneration_start_age)/( max(lifespan-degeneration_start_age,0.0001) )))

    # Increase metabolism
    metabolism = agent.GetProperty("sugar_metabolism")
    metabolism = metabolism * (1+ageDegenerationFactor)
    agent.SetProperty("sugar_metabolism", metabolism)

    metabolism = agent.GetProperty("spice_metabolism")
    metabolism = metabolism * (1+ageDegenerationFactor)
    agent.SetProperty("spice_metabolism", metabolism)

    # Decrease vision
    vision = agent.GetProperty("vision")
    vision = vision * (1-ageDegenerationFactor)
    agent.SetProperty("vision", int(vision))

    # random mortality chance
    # if (random.randint(0,100) < ageDegenerationFactor*100):
    #     sugarscape.KillAgent(agent, "old_age_mortality_chance")
    #     return
    
    # Increase random cultural de-generation factor
    myTag: List[int]  = agent.GetProperty("culture_tag")
    for i in range(0, len(myTag)):
        if (random.randint(0,100) < ageDegenerationFactor*100):
            myTag[i] = random.randint(0,1)

    agent.SetProperty("culture_tag", myTag)

    # Decrease immune system strength with aging
    immune_string = agent.GetProperty("immune_string")
    immune_string = immune_string[0:int(len(immune_string)*(1-ageDegenerationFactor))]
    
        
        

