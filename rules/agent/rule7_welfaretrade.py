from typing import List, Tuple, Callable
from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass
            

def Step(sugarscape: Sugarscape, agent: Agent):
    #visionVectors: List[Tuple[int]] = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    welfareFunc = sugarscape.GetHyperFunction("welfare_function")
    
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

        #factor culture in later

        #compute MRS, if equal to neigbout MRS continue
        myMRS = CalculateMRS(agent)
        neighbourMRS = CalculateMRS(neighbour)

        #if they are equal, end
        if myMRS == neighbourMRS:
            continue
        if myMRS == 0 or neighbourMRS == 0:
            continue
        #spice flows from high MRS to low MRS
        #sugar flows from low MRS to high MRS

        #Calculate geometric mean of MRS to get price p
        p = (myMRS * neighbourMRS) ** 0.5

        if p == 0:
            continue

        #Calculate amount to trade
        # if p > 1 then trade p units of spice for 1 unit of sugar
        # if p < 1 then trade 1/p units of sugar for 1 unit of spice
        if p > 1:
            spiceToTrade = p
            sugarToTrade = 1
        else:
            spiceToTrade = 1
            sugarToTrade = 1/p

        # if trade makes agents both better off (increases MRS) and doesn't cause MRS's to cross, then trade

        #first assuming agent is the one with the higher MRS
        traders = [agent, neighbour]
        
        #then if agentNeigbour has higher MRS, swap
        if myMRS < neighbourMRS:
            traders = [neighbour, agent]

        spiceFrom = traders[0]
        sugarFrom =  traders[1]

        #get welfare before and after trade
        curr_welfare1 = welfareFunc(spiceFrom, 0, 0)
        curr_welfare2 = welfareFunc(sugarFrom, 0, 0)
        welfare_after_trade1 = welfareFunc(spiceFrom, sugarToTrade, -spiceToTrade)
        welfare_after_trade2 = welfareFunc(sugarFrom, -sugarToTrade, spiceToTrade)

        #check if trade makes both agents better off (increases welfare)
        if welfare_after_trade1 <= curr_welfare1 and welfare_after_trade2 <= curr_welfare2:
            continue

        #check if trade doesn't cause MRS's to cross. 
        # if statement below doesn't 
        if curr_welfare1 > curr_welfare2 and welfare_after_trade1 < welfare_after_trade2:
            continue

        if curr_welfare1 < curr_welfare2 and welfare_after_trade1 > welfare_after_trade2:
            continue


        # do the trade
        spiceFrom.SetProperty("spice_wealth", spiceFrom.GetProperty("spice_wealth") - spiceToTrade)
        sugarFrom.SetProperty("sugar_wealth", sugarFrom.GetProperty("sugar_wealth") - sugarToTrade)
        spiceFrom.SetProperty("sugar_wealth", spiceFrom.GetProperty("sugar_wealth") + sugarToTrade)
        sugarFrom.SetProperty("spice_wealth", sugarFrom.GetProperty("spice_wealth") + spiceToTrade)
        print("Trade made")
        #end loop
        # Can only trade once per step
        return


def CalculateMRS(agent: Agent):
    if agent.GetProperty("sugar_wealth") == 0:
        return 0
    if agent.GetProperty("sugar_wealth") == 0:
        return 0
    
    timeToSugarDeath = agent.GetProperty("sugar_wealth") / agent.GetProperty("sugar_metabolism")
    timeToSpiceDeath = agent.GetProperty("spice_wealth") / agent.GetProperty("spice_metabolism")

    return timeToSpiceDeath / timeToSugarDeath