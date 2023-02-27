from __future__ import annotations
import random
import threading
import matplotlib.pyplot as plt
from core.lib import *
from core.agent import Agent
import time

s = Sugarscape(100)
s.AddAgents(750)
s.CreateScape(Attribute("sugar", 0, 100))
s.CreateScape(Attribute("pollution", 0, 100))

s.GetScape("sugar").FillWithPerlinNoise(octaves=4)
s.GetScape("sugar").Normalise(True)

s.GetScape("sugar").DefaultValuesByCutOff(70,False, True, 0.5)

import rules.scape.rule_seasonal_growback as growback 
s.AddScapeRule("sugar", growback.Init, growback.Step, growback.CellStep)
 
import rules.scape.rule_diffusion as dif 
#s.AddScapeRule("pollution", dif.Init, dif.Step, dif.CellStep)
 
import rules.agent.rule0_metabolism as rule0
s.AddAgentRule(rule0.Init, rule0.Step)

import rules.agent.rule1_movement as rule1
s.AddAgentRule(rule1.Init, rule1.StepPollutionModified)

import rules.agent.rule2_agent_replacement as rule2
s.AddAgentRule(rule2.Init, rule2.Step)

import rules.agent.rule3_pollution_formation as rule3
#s.AddAgentRule(rule3.Init, rule3.Step)

import rules.agent.rule4_sex as rule4
s.AddAgentRule(rule4.Init, rule4.Step)

import rules.agent.rule5_cultural_transmission as rule5
s.AddAgentRule(rule5.Init, rule5.Step)

import rules.agent.rule6_combat as rule6
#s.AddAgentRule(rule6.Init, rule6.Step)

s.SetHyperParameter("min_metabolism", 10)
s.SetHyperParameter("max_metabolism", 20)
s.SetHyperParameter("max_vision", 4)
s.SetHyperParameter("initial_endowment_range", (50, 100))
s.SetHyperParameter("life_span_range", (60, 100))
s.SetHyperParameter("season_change_time", 50)
s.SetHyperParameter("sugar_growback_amount", 50)
s.SetHyperParameter("male_fertile_age_range", (12, 15 , 50, 60))
s.SetHyperParameter("female_fertile_age_range", (12, 15, 40, 50))
s.SetHyperParameter("pollution_per_sugar", 0.2)
s.SetHyperParameter("diffusion_rate", 1.05)
s.SetHyperParameter("cultural_tag_length", 11)

# Find the similarity between 2 binary strings
# Based on number of ones and their positions
def CulturalSimilarityFunction(culturalTag1: List[int], culturalTag2: List[int]) -> float:
    # count the number of 1's in the tag
    one_count1 = culturalTag1.count(1)
    one_count2 = culturalTag2.count(1)
    one_count_diff = abs(one_count1 - one_count2)

    # count the number of 1's in the same position
    same_position_count = 0
    for i in range(len(culturalTag1)):
        if culturalTag1[i] == culturalTag2[i]:
            same_position_count += 1

    # return the similarity
    return 1 - (one_count_diff + (len(culturalTag1) - same_position_count)) / (2 * len(culturalTag1))

s.SetHyperFunction("cultural_similarity_function", CulturalSimilarityFunction)
s.SaveEpochs(True, 0)


SIM_TIME = 100
s.RunSimulation(SIM_TIME)
saveStates = s.GetScapeSaveStates()
agentStates = s.GetAgentSaveStates()


def Func(scape:Scape, _:int):
    return scape.FilledValueCount(True)

PlotScape.LinePlotAttributesOverTimeSteps(Func,s,"agents",saveStates, True)

PlotScape.AnimPlotTimeSteps(s, "agents", saveStates)    

PlotScape.AnimPlotTimeSteps(s, "sugar", saveStates)   
PlotScape.AnimPlotTimeSteps(s, "pollution", saveStates)      
#plots = ["sugar"]
#PlotScape.CurrentStatePlot(s, plots)

def colorByVision(agent:Agent):
    vision = agent.GetProperty("vision")
    if vision > 0 and vision <= 2:
        return 0
    elif vision > 2:
        return 1
    

def colorByTribe(agent:Agent):
    tribe = agent.GetProperty("tribe")
    if tribe == "red":
        return 0
    elif tribe == "blue":
        return 1

# use k means to cluster the tags into distinct groups based on cultural similarity threshold
def groupAgentsByCultureTags(agents: List[Agent], threshold: float = 1) -> Dict[int, List[int]]:
    # define hash table to store cluster tags
    # Dict of group index to list of agents ids
    agent_groups: Dict[int, List[int]] = {}
    # get number of clusters
    num_clusters = 0

    # select first tag as first cluster
    cluster_tag = agents[0].GetProperty("culture_tag")
    clusterIndex = 0

    while len(agents)-1 != len(agent_groups):
        newClusterTag = None
        # loop through all tags and compare to cluster tag, check if cultural similarity is less than threshold
        for i in range(len(agents[1:])):
            if str(agents[i].GetProperty("culture_tag")) in agent_groups:
                continue
            if CulturalSimilarityFunction(cluster_tag, agents[i].GetProperty("culture_tag")) < threshold:
                # Not in cluster
                num_clusters += 1
                newClusterTag = agents[i].GetProperty("culture_tag")
            else:
                # In cluster
                if clusterIndex not in agent_groups:
                    agent_groups[clusterIndex] = []

                agent_groups[clusterIndex].append(agents[i].id)
    
        cluster_tag = newClusterTag
        clusterIndex += 1
        #print(len(agent_groups), len(agents))
    return agent_groups


#PlotScape.AnimPlotAgentAttributeTimeSteps(s, saveStates, agentStates, colorByVision)
PlotScape.AnimPlotAgentAttributeTimeSteps(s, saveStates, agentStates, colorByTribe)
#PlotScape.PrintAgentPropertyMean(s, range(0, SIM_TIME), ["vision", "metabolism"], agentStates)
PlotScape.AnimPlotAgentGrouping(s, range(0, SIM_TIME), ["vision", "metabolism"], agentStates)
plt.show()