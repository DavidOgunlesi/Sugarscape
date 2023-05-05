from typing import List, Tuple, Callable
from core.agent import Agent
from core.sugarscape import Sugarscape
import random

def Init(sugarscape: Sugarscape, agent: Agent):
    pass

def Step(sugarscape: Sugarscape, agent: Agent):
    # If above adulthood age threshold, allow the agent to become altruistic
    age = agent.GetProperty("age")
    adulthood_age = sugarscape.GetHyperParameter("adulthood_age")
    if (age < adulthood_age):
        return
    
    reciprocative = agent.GetProperty("reciprocative")

    mrsFunc = sugarscape.GetHyperFunction("mrs_function")
    welfareFunc = sugarscape.GetHyperFunction("welfare_function")
    age_adjusted_welfareFunc = sugarscape.GetHyperFunction("aawi_function")
    myMRS = mrsFunc(agent)
    myWelfare = welfareFunc(agent, 0, 0)

    # Get neighbours
    neighbours = agent.GetAgentNeighbours()
    random.shuffle(neighbours) # Needs to be shuffled to prevent bias

    if len(neighbours) == 0:
        return
    
    # If designated reciprocative
    if reciprocative:
        
        lowest_aaw = 100000
        lowest_aaw_neighbour = None

        # For all neighbours as for as vision permits, find the one with the lowest Age-Adjusted Welfare Index
        for neighbourID in neighbours:
            neighbour = sugarscape.GetAgentFromId(neighbourID)
            if neighbour == None:
                continue
            if neighbour.GetProperty("dead") == 1:
                continue
            neighbour_welfare = age_adjusted_welfareFunc(neighbour)
            if neighbour_welfare < lowest_aaw:
                lowest_aaw = neighbour_welfare
                lowest_aaw_neighbour = neighbour
        
        if lowest_aaw_neighbour == None:
            return
        
        # Transfer sugar/spice to this neighbour
        # If they have higher MRS, given them sugar
        # If they have lower MRS, given them spice
        print("Agent " + str(agent.id) + " is transferring resources to agent " + str(lowest_aaw_neighbour.id))
        sugarscape.AddStats("altruism_share", 1)

        amount = sugarscape.GetHyperParameter("altruism_donation_amount")
        if myMRS > mrsFunc(lowest_aaw_neighbour):
            agent.SetProperty("sugar_wealth", agent.GetProperty("sugar_wealth") - amount)
            lowest_aaw_neighbour.SetProperty("sugar_wealth", lowest_aaw_neighbour.GetProperty("sugar_wealth") + amount)

        else:
            agent.SetProperty("spice_wealth", agent.GetProperty("spice_wealth") - amount)
            lowest_aaw_neighbour.SetProperty("spice_wealth", lowest_aaw_neighbour.GetProperty("spice_wealth") + amount)
        

    reciprocativeNeighbours = countNeighbourProperty(sugarscape, agent, neighbours, "reciprocative")
    totalNeighbours = len(neighbours)

    # If resource welfare falls below a threshold, agent becomes defective
    if myWelfare < sugarscape.GetHyperParameter("altrusim_reciprocative_welfare_threshold"):
        agent.SetProperty("reciprocative", False)
        return
    
    if reciprocativeNeighbours > totalNeighbours/2:
        #If the majority of neighbours are reciprocating, randomly designate altruism on the agent
        agent.SetProperty("reciprocative", True)
        return
    else:
        # If the majority of neighbours are defective, randomly designate defective on the agent
        agent.SetProperty("reciprocative", False)
        return
    

def countNeighbourProperty(sugarscape: Sugarscape, agent: Agent, neighbours: List[int], prop: str):
    count = 0
    for neighbourID in neighbours:
        neighbour = sugarscape.GetAgentFromId(neighbourID)
        if neighbour == None:
            continue
        if neighbour.GetProperty("dead") == 1:
            continue
        if neighbour.GetProperty(prop) != None:
            count += 1
    return count
        
        

