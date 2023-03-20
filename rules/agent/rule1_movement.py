from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    max = sugarscape.GetHyperParameter("max_vision")
    
    if agent.GetProperty("vision") == None:
        agent.SetProperty("vision", random.randint(1, max))

def Step(sugarscape: Sugarscape, agent: Agent):
    visionVectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    visionVectors2 = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    bestSugarValue = (-1, (0, 0))
    
    visionVectors = visionVectors2
    
    # Needs to be shuffled to prevent bias
    random.shuffle(visionVectors)
    
    # Look  out as far as vision allows and find the best sugar value
    for i in range(1, agent.GetProperty("vision")+1):
        for v in visionVectors:
            x = agent.x + (v[0] * i)
            y = agent.y + (v[1] * i)
            
            if not agent.scape.IsInBounds(x, y):
                continue
            
            val = sugarscape.GetScape("sugar").GetValue(x, y)
            
            #IF the sugar value is better than the current best, set it as the best
            if val > bestSugarValue[0] and sugarscape.GetScape("agents").IsCellDefault(x, y):
                bestSugarValue = (val, (x, y))
                
            # We don't need to check if sugar value is equal because we 
            # look a positions in order of distance from the agent
            
        # Move to best sugar value
        newx, newy = bestSugarValue[1][0], bestSugarValue[1][1]
        if bestSugarValue[0] != -1 and agent.scape.IsInBounds(newx, newy) and agent.scape.IsCellDefault(newx, newy):
            agent.MoveTo(newx, newy)
         
def StepPollutionModified(sugarscape: Sugarscape, agent: Agent):
    visionVectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    visionVectors2 = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    bestSugarValue = (-1, (0, 0))
    
    visionVectors = visionVectors2
    
    # Needs to be shuffled to prevent bias
    random.shuffle(visionVectors)
    
    # Look  out as far as vision allows and find the best sugar value
    for i in range(1, agent.GetProperty("vision")+1):
        for v in visionVectors:
            x = agent.x + (v[0] * i)
            y = agent.y + (v[1] * i)
            
            if not agent.scape.IsInBounds(x, y):
                continue
            
            sugarVal = sugarscape.GetScape("sugar").GetValue(x, y)
            polVal = sugarscape.GetScape("pollution").GetValue(x, y)
            val = sugarVal/max(polVal, 1)
            #IF the sugar:pollution ratio is better than the current best, set it as the best
            if val > bestSugarValue[0] and sugarscape.GetScape("agents").IsCellDefault(x, y):
                bestSugarValue = (val, (x, y))
                
            # We don't need to check if sugar value is equal because we 
            # look a positions in order of distance from the agent
            
        # Move to best sugar to pollution value
        newx, newy = bestSugarValue[1][0], bestSugarValue[1][1]
        if bestSugarValue[0] != -1 and agent.scape.IsInBounds(newx, newy) and agent.scape.IsCellDefault(newx, newy):
            agent.MoveTo(newx, newy)

def StepPollutionAndWelfareModified(sugarscape: Sugarscape, agent: Agent):
    visionVectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    visionVectors2 = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    bestSugarValue = (-1, (0, 0))
    
    visionVectors = visionVectors2
    
    # Needs to be shuffled to prevent bias
    random.shuffle(visionVectors)
    welfareFunc = sugarscape.GetHyperFunction("welfare_function")
    # Look  out as far as vision allows and find the best sugar value
    for i in range(1, agent.GetProperty("vision")+1):
        for v in visionVectors:
            x = agent.x + (v[0] * i)
            y = agent.y + (v[1] * i)
            
            if not agent.scape.IsInBounds(x, y):
                continue
            
            sugarVal = sugarscape.GetScape("sugar").GetValue(x, y)
            polVal = sugarscape.GetScape("pollution").GetValue(x, y)
            welfare = welfareFunc(agent, sugarVal, 0)
            val = welfare/max(polVal, 1)

            #If the sugar:pollution ratio is better than the current best, set it as the best
            if val > bestSugarValue[0] and sugarscape.GetScape("agents").IsCellDefault(x, y):
                bestSugarValue = (val, (x, y))
                
            # We don't need to check if sugar value is equal because we 
            # look a positions in order of distance from the agent
            
        # Move to best sugar to pollution value
        newx, newy = bestSugarValue[1][0], bestSugarValue[1][1]
        if bestSugarValue[0] != -1 and agent.scape.IsInBounds(newx, newy) and agent.scape.IsCellDefault(newx, newy):
            agent.MoveTo(newx, newy)