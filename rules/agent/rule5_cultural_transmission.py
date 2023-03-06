from core.agent import Agent
from core.sugarscape import Sugarscape
import random
from typing import List
from rules.agent.global_agent_funcs import CulturalSimilarityFunction

def Init(sugarscape: Sugarscape, agent: Agent):
    #print("INIT: ", agent.GetProperty("culture_tag") == None)
    if agent.GetProperty("culture_tag") == None:
        agent.SetProperty("culture_tag", rand_key(sugarscape.GetHyperParameter("cultural_tag_length"), agent.id))

    #print(agent.GetProperty("culture_tag"))

def Step(sugarscape: Sugarscape, agent: Agent):
    visionVectors = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    
    for neighbour in GetNeighbours(sugarscape, agent, visionVectors):
        # For each neighbour a random flag is selected and compared to the agent's flag
        myTag: List[int]  = agent.GetProperty("culture_tag")
        neighbourTag: List[int] = neighbour.GetProperty("culture_tag")
        if neighbourTag == None:
            print(">", neighbour.properties)
        randomFlag = random.randint(0, len(neighbourTag)-1)
        
        # if the neighbours flag disagrees with agents flag, the neighbour adopts the agents flag
        if neighbourTag[randomFlag] != myTag[randomFlag]:
            neighbourTag[randomFlag] = myTag[randomFlag]
            neighbour.SetProperty("culture_tag", neighbourTag)
            
    agent.SetProperty("tribe", ResolveTribe(agent.GetProperty("culture_tag")))  
            
def ResolveTribe(culturalTag: List[int]):
    # count the number of 1's in the tag
    one_count = culturalTag.count(1)
    if one_count > len(culturalTag) / 2:
        return "red"
    
    return "blue"
      
      
def GetNeighbours(sugarscape: Sugarscape, agent: Agent, visionVectors):
    neighbors = []
    for i in range(1, agent.GetProperty("vision")+1):
        for v in visionVectors:
            x = agent.x + (v[0] * i)
            y = agent.y + (v[1] * i)
            
            agentNeigbour = sugarscape.GetAgentAtPosition(agent.x + x, agent.y + y)
            if agentNeigbour != None:
                neighbors.append(agentNeigbour) 
                
    return neighbors   


# Function to create the
# random binary string
def rand_key(p, seed=0):
   
    # Variable to store the
    # string
    key1 = []
 
    # Loop to find the string
    # of desired length
    for _ in range(p):
         
        # randint function to generate
        # 0, 1 randomly and converting
        # the result into str
        random.seed(seed)
        temp = random.randint(0, 1)
 
        # Concatenation the random 0, 1
        # to the final result
        key1.append(temp)
         
    return(key1)