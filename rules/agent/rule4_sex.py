from core.agent import Agent
from core.sugarscape import Sugarscape
import random
from typing import List, Tuple

def Init(sugarscape: Sugarscape, agent: Agent):
    agent.SetProperty("fertile", False)
    agent.SetProperty("sex", random.choice(["male", "female"]))

def Step(sugarscape: Sugarscape, agent: Agent):
    age = agent.GetProperty("age")
    
    visionVectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    
    # Become fertile at certain age and lose fertility after certain age
    if agent.GetProperty("sex") == "male":
        fert = sugarscape.GetHyperParameter("male_fertile_age_range") 
    else:
        fert = sugarscape.GetHyperParameter("female_fertile_age_range") 
    min_start_fert, max_start_fert, min_end_fert, max_end_fert = fert
    start_fert = random.randint(min_start_fert, max_start_fert)
    end_fert = random.randint(min_end_fert, max_end_fert)
    agent.SetProperty("fertile", age > start_fert and age < end_fert)
    
    if agent.GetProperty("fertile") == False:
        return
    
    # If there is a fertile agent in the neighborhood, reproduce
    # neighbors = GetNeighbours(sugarscape, agent, visionVectors)
    neighbours = agent.GetAgentNeighbours()
     # Needs to be shuffled to prevent bias
    random.shuffle(neighbours)
    
    if len(neighbours) == 0:
        return
                
    Breed(neighbours, sugarscape, agent, visionVectors)
    

# def GetNeighbours(sugarscape: Sugarscape, agent: Agent, visionVectors):
#     neighbors = []
#     for i in range(1, agent.GetProperty("vision")+1):
#         for v in visionVectors:
#             x = agent.x + (v[0] * i)
#             y = agent.y + (v[1] * i)
            
#             agentNeigbour = sugarscape.GetAgentAtPosition(agent.x + x, agent.y + y)
#             if agentNeigbour != None:
#                 neighbors.append(agentNeigbour) 
                
#     return neighbors
        
def Breed(neighbours: List[int], sugarscape: Sugarscape, agent: Agent, visionVectors):       
    potentialMateID:int = random.choice(neighbours)
    potentialMate:Agent = sugarscape.GetAgentFromId(potentialMateID)
    
    if potentialMate == None:
        return
    
    mateFertile = potentialMate.GetProperty("fertile")
    mateSex = potentialMate.GetProperty("sex")
    meFertile = agent.GetProperty("fertile")
    mySex = agent.GetProperty("sex")
    # if potential mate is fertile and of opposite sex
    if meFertile == True and mateFertile == True and mateSex != mySex:
        # If there is a sutiable site to have child
            for x, y in visionVectors:
                newx = agent.x + x
                newy = agent.y + y
                if agent.scape.IsInBounds(newx, newy) and agent.scape.IsCellDefault(newx, newy):
                    child = sugarscape.BirthNewAgentAtPos(newx, newy)
                    sugarscape.AddStats("births", 1)
                    MixAndSetGenetics(child, agent, potentialMate, ["sugar_metabolism","spice_metabolism", "vision", "culture_tag", "immune_string"])
                    break

def MixAndSetGenetics(child: Agent, parent1:Agent, parent2: Agent, propsToMix:List[str] = None):
    props1 = parent1.GetAllProperties(propsToMix)
    props2 = parent2.GetAllProperties(propsToMix)
    props = zip(props1, props2)
    parents = [parent1, parent2]
    #Select from random parent
    for propChoice in props:
        chosenPropIndex = random.choice([0, 1])
        chosenPropParent = parents[chosenPropIndex]
        chosenPropStr = propChoice[chosenPropIndex]
        val = chosenPropParent.GetProperty(chosenPropStr)
        child.SetProperty(chosenPropStr, val)