from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass
            

def Step(sugarscape: Sugarscape, agent: Agent):
    visionVectors = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    
    # Needs to be shuffled to prevent bias
    random.shuffle(visionVectors)
    # Look  out as far as vision allows and ignore sites with members of my own tribe
    best_site = None
    best_reward = 0
    for i in range(1, agent.GetProperty("vision")+1):
        for v in visionVectors:
            x = agent.x + (v[0] * i)
            y = agent.y + (v[1] * i)
            
            if not agent.scape.IsInBounds(x, y):
                continue
            
            agentNeigbour = sugarscape.GetAgentAtPosition(x, y)
            if agentNeigbour == None:
                continue

            similarity = sugarscape.GetHyperFunction("cultural_similarity_function")(agentNeigbour.GetProperty("culture_tag"), agent.GetProperty("culture_tag"))
            
            # Ignore all sites occupied by members of my own tribe
            if similarity >= 0.5:
                continue
            
            # Throw out all sites occupied by members of other tribes who are wealthier than me
            if similarity < 0.5 and agentNeigbour.GetProperty("sugar_wealth") > agent.GetProperty("sugar_wealth"):
                continue
            # if the site has an agent next to it (vunerable to retaliation), ignore it
            for i in [ (0, -1), (-1, 0), (1, 0), (0, 1)]:
                if sugarscape.GetAgentAtPosition(x + i[0], y + i[1]) != None:
                    continue

            reward = sugarscape.GetScape("sugar").GetValue(x, y)
            # if site is occupied add minimun of agents wealth and max sugar i can hold
            if agentNeigbour != None:
                reward += agent.GetProperty("sugar_wealth") #min(agent.GetProperty("sugar_wealth"), sugarscape.GetHyperParameter("max_sugar_hold"))

            if best_reward < reward:
                best_reward = reward
                best_site = (x, y)

    (newx, newy) = best_site
    if best_site != None and agent.scape.IsInBounds(newx, newy) and agent.scape.IsCellDefault(newx, newy):
        agent.MoveTo(newx, newy)
        # collect sugar at site
        sugarValue = sugarscape.GetScape("sugar").GetValue(newx, newy)
        agent.SetProperty("sugar_gathered", sugarValue)
        
        # Remove all sugar at site
        sugarscape.GetScape("sugar").SetDefault(newx, newy)

        # kill agent if there is one there
        agentNeigbour = sugarscape.GetAgentAtPosition(newx, newy)
        if agentNeigbour != None:
            sugarscape.KillAgent(agentNeigbour)
            