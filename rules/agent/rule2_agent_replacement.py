from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    minAge = sugarscape.GetHyperParameter("min_life_span")
    maxAge = sugarscape.GetHyperParameter("max_life_span")
    agent.SetProperty("life_span", random.randint(minAge, maxAge))
    agent.SetProperty("age", 0)

def Step(sugarscape: Sugarscape, agent: Agent):
    age = agent.GetProperty("age")
    max_age = agent.GetProperty("life_span")
    newAge = age + 1
    agent.SetProperty("age", newAge)
    
    if newAge > max_age:
        #Kill & Create Replacement
        sugarscape.KillAgent(agent)
        
    if agent.GetProperty("dead") == 1:
        sugarscape.AddNewAgent()
        
        
        
         