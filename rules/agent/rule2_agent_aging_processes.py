from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    minAge, maxAge = sugarscape.GetHyperParameter("life_span_range")
    
    if agent.GetProperty("life_span") == None:
        agent.SetProperty("life_span", random.randint(minAge, maxAge))
        
    agent.SetProperty("age", 0)

def Step(sugarscape: Sugarscape, agent: Agent):
    age = agent.GetProperty("age")
    max_age = agent.GetProperty("life_span")
    newAge = age + 1
    agent.SetProperty("age", newAge)
    
    if newAge > max_age:
        #Kill & Create Replacement
        sugarscape.KillAgent(agent, "old_age")
        
    # if agent.GetProperty("dead") == 1:
    #     sugarscape.AddNewAgent()
        
        
        
         