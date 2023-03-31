from typing import List, Tuple, Callable
from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass
            

def Step(sugarscape: Sugarscape, agent: Agent):
    visionVectors: List[Tuple[int]] = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    
    # Needs to be shuffled to prevent bias
    random.shuffle(visionVectors)
    # Look  out as far as vision allows and ignore sites with members of my own tribe
    simFunc: Callable = sugarscape.GetHyperFunction("cultural_similarity_function")
    myCultureTag = agent.GetProperty("culture_tag")
    cultureThreshold = sugarscape.GetHyperParameter("cultural_similarity_threshold")
    best_site = None
    best_reward = 0
    
    neighbours = agent.GetAgentNeighbours()
     # Needs to be shuffled to prevent bias
    random.shuffle(neighbours)
    
    if len(neighbours) == 0:
        return
    
    for neighbourID in neighbours:
        
        neighbour = sugarscape.GetAgentFromId(neighbourID)
        
        if neighbour == None:
            continue
        
        if neighbour.GetProperty("dead") == 1:
            continue

        similarity = simFunc(neighbour.GetProperty("culture_tag"), myCultureTag)
        
        # Ignore all sites occupied by members of my own tribe
        if similarity >= cultureThreshold:
            continue
        
        # Throw out all sites occupied by members of other tribes who are wealthier than me
        if similarity < cultureThreshold and neighbour.GetProperty("sugar_wealth") > agent.GetProperty("sugar_wealth"):
            continue

        # if the site has an agent next to it (vunerable to retaliation), ignore it
        for v2 in visionVectors:
            agentAtPos = sugarscape.GetAgentAtPosition(neighbour.x + v2[0], neighbour.y + v2[1])

            # If there is an agent at the site and they are of a different tribe, ignore it
            if agentAtPos != None and simFunc(agentAtPos.GetProperty("culture_tag"), myCultureTag) < cultureThreshold:
                continue

        reward = neighbour.GetProperty("sugar_wealth")  #sugarscape.GetScape("sugar").GetValue(x, y)

        if best_reward < reward:
            best_reward = reward
            best_site = (neighbour.x, neighbour.y)

    if best_site is None:
        return
    
    (newx, newy) = best_site
    if best_site != None and agent.scape.IsInBounds(newx, newy):
        agentToAttack = sugarscape.GetAgentAtPosition(newx, newy)
        
        if agentToAttack == None:
            return

        # collect agents sugar
        sugarValue = agentToAttack.GetProperty("sugar_wealth")
        agent.SetProperty("sugar_gathered", sugarValue)
        agent.ModifyProperty("sugar_wealth", sugarValue)
        
        # Remove all sugar at site
        sugarscape.GetScape("sugar").SetDefault(newx, newy)

        # kill agent
        sugarscape.KillAgent(agentToAttack)
        #print("Agent killed in warfare")
        
        agent.MoveTo(newx, newy)
            