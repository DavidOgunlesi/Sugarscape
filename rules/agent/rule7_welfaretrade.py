from typing import List, Tuple, Callable
from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass
            

def Step(sugarscape: Sugarscape, agent: Agent):
    
    welfareFunc = sugarscape.GetHyperFunction("welfare_function")
    mrsFunc = sugarscape.GetHyperFunction("mrs_function")
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
        myMRS = mrsFunc(agent)
        neighbourMRS = mrsFunc(neighbour)

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

        if isinstance(welfare_after_trade1, complex) or isinstance(welfare_after_trade2, complex):
            continue

        #check if trade makes both agents better off (increases welfare)
        if welfare_after_trade1 <= curr_welfare1 and welfare_after_trade2 <= curr_welfare2:
            continue

        #check if trade doesn't cause MRS's to cross. 
        # if statement below doesn't 
        if curr_welfare1 > curr_welfare2 and welfare_after_trade1 < welfare_after_trade2:
            continue

        if curr_welfare1 < curr_welfare2 and welfare_after_trade1 > welfare_after_trade2:
            continue

        # set stats
        sugarscape.AddStats("total_trade_count", 1)
        sugarscape.AddStats("total_sugar_trade_fromagent_wealth", spiceFrom.GetProperty("sugar_wealth"))
        sugarscape.AddStats("total_sugar_trade_toagent_wealth", sugarFrom.GetProperty("sugar_wealth"))
        sugarscape.AddStats("total_spice_trade_fromagent_wealth", sugarFrom.GetProperty("spice_wealth"))
        sugarscape.AddStats("total_spice_trade_toagent_wealth", spiceFrom.GetProperty("spice_wealth"))
        #metabolic rates
        sugarscape.AddStats("total_sugar_trade_fromagent_metabolism", spiceFrom.GetProperty("sugar_metabolism"))
        sugarscape.AddStats("total_sugar_trade_toagent_metabolism", sugarFrom.GetProperty("sugar_metabolism"))
        sugarscape.AddStats("total_spice_trade_fromagent_metabolism", sugarFrom.GetProperty("spice_metabolism"))
        sugarscape.AddStats("total_spice_trade_toagent_metabolism", spiceFrom.GetProperty("spice_metabolism"))

        # do the trade
        spiceFrom.SetProperty("spice_wealth", spiceFrom.GetProperty("spice_wealth") - spiceToTrade)
        sugarFrom.SetProperty("sugar_wealth", sugarFrom.GetProperty("sugar_wealth") - sugarToTrade)
        spiceFrom.SetProperty("sugar_wealth", spiceFrom.GetProperty("sugar_wealth") + sugarToTrade)
        sugarFrom.SetProperty("spice_wealth", sugarFrom.GetProperty("spice_wealth") + spiceToTrade)
        
        # trade made
        #print("Trade made")
        #end loop
        # Can only trade once per step
        return