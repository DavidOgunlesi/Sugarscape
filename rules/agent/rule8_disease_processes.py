from typing import List, Tuple, Callable
from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    
    agent.SetProperty("diseases", [])
    
    # Give agents immune system string
    if agent.GetProperty("immune_string") == None:
        max = sugarscape.GetHyperParameter("max_immune_string_length")
        min = sugarscape.GetHyperParameter("min_immune_string_length")
        length = random.randint(min, max)
        agent.SetProperty("immune_string", agent.rand_key(length, agent.id))


def Step(sugarscape: Sugarscape, agent: Agent):
    # Get disease pool
    disease_pool = sugarscape.GetHyperParameter("disease_pool")
    currentCodedDisease = None
    
    if random.random() > sugarscape.GetHyperParameter("disease_infection_chance"):
        # Random chance of getting infected
        currentCodedDisease = random.choice(disease_pool)
    else:
        # Random neighbour infection chance
        neighbours = agent.GetAgentNeighbours()
        for neighbourID in neighbours:
            neighbourAgent = sugarscape.GetAgentFromId(neighbourID)
            
            if neighbourAgent == None:
                continue
            
            if not neighbourAgent.GetProperty("infected"):
                continue
            
            diseases = neighbourAgent.GetProperty("diseases")
            
            if len(diseases) == 0:
                continue
            
            disease = random.choice(diseases)
            
            if random.random() > disease["infection_chance"]:
                currentCodedDisease = disease
    
    if currentCodedDisease == None:
        return
    
    # if disease is a substring of immune string, agent is immune
    if currentCodedDisease["string"] in agent.GetProperty("immune_string"):
        sugarscape.AddStats("immune", 1)
        # print("Agent " + str(agent.id) + " is immune to " + currentCodedDisease["name"])
        return
    
    # Agent is infected
    agent.SetProperty("infected", True)
    # print("Agent " + str(agent.id) + " is infected with " + currentCodedDisease["name"])
    diseases = agent.GetProperty("diseases")
    diseases.append(currentCodedDisease)
    agent.SetProperty("diseases", diseases)
    
    # Get agent's immune system string
    immune_string = agent.GetProperty("immune_string")
    
    #find closes hamming distance substring to immune string
    hamming_distance_func = sugarscape.GetHyperFunction("hamming_distance")
    dString = currentCodedDisease["string"]
    
    bestHammingDistance = {"dist": 9999, "index": 0}
    
    for i in range(0, len(immune_string) - len(dString) + 1):
        hammingDistance = hamming_distance_func(dString, immune_string[i:i+len(dString)])
        if hammingDistance < bestHammingDistance["dist"]:
            bestHammingDistance = {"dist": hammingDistance, "index": i}
    
    index = bestHammingDistance["index"]
    # Change first bit of substring to 1
    immune_string[index] = '1' if immune_string[index] == '0' else '0'
    
    # Set agent's immune system string
    agent.SetProperty("immune_string", immune_string)

    # random mortality chance
    if (random.randint(0,100) < currentCodedDisease["mortality_chance"]*100):
        sugarscape.KillAgent(agent, "disease")
        return
    
    
        
        

