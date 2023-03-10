from __future__ import annotations
import matplotlib.pyplot as plt
from core.lib import *
from core.agent import Agent
from core.plotscape import PlotScape

print(" Creating Sugarscape...")
s = Sugarscape(100)

print(" Adding Agents...")
s.AddAgents(750)

print(" Creating Scapes...")
s.CreateScape(Attribute("sugar", 0, 100))
s.CreateScape(Attribute("pollution", 0, 100))

print(" Filling Scapes...")
s.GetScape("sugar").FillWithPerlinNoise(octaves=1) # 4
s.GetScape("sugar").Normalise(True)
s.GetScape("sugar").DefaultValuesByCutOff(70,False, True, 0.1)

print(" Adding Rules...")

import rules.scape.rule_growback as growback 
s.AddScapeRule("sugar", growback.Init, growback.Step, growback.CellStep)

import rules.scape.rule_seasonal_growback as seasonal_growback 
#s.AddScapeRule("sugar", seasonal_growback.Init, seasonal_growback.Step, seasonal_growback.CellStep)
 
import rules.scape.rule_diffusion as dif 
#s.AddScapeRule("pollution", dif.Init, dif.Step, dif.CellStep)
 
import rules.agent.rule0_metabolism as rule0
s.AddAgentRule(rule0.Init, rule0.Step)

import rules.agent.rule1_movement as rule1
s.AddAgentRule(rule1.Init, rule1.StepPollutionModified)

import rules.agent.rule2_agent_replacement as rule2
#s.AddAgentRule(rule2.Init, rule2.Step)

import rules.agent.rule3_pollution_formation as rule3
#s.AddAgentRule(rule3.Init, rule3.Step)

import rules.agent.rule4_sex as rule4
#s.AddAgentRule(rule4.Init, rule4.Step)

import rules.agent.rule5_cultural_transmission as rule5
s.AddAgentRule(rule5.Init, rule5.Step)

import rules.agent.rule6_combat as rule6
s.AddAgentRule(rule6.Init, rule6.Step)

print(" Setting Hyperparameters...")
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
s.SetHyperParameter("cultural_similarity_threshold", 0.7)

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


SIM_TIME = 10

print("Created Sugarscape...")
print("Starting Simulation...")
s.RunSimulation(SIM_TIME)
scapeStates = s.GetScapeSaveStates()
agentStates = s.GetAgentSaveStates()


def Func(scape:Scape, _:int):
    return scape.FilledValueCount(True)

PlotScape.LinePlotAttributesOverTimeSteps(Func,s,"agents",scapeStates, True)

PlotScape.AnimPlotTimeSteps(s, "agents", scapeStates)    

PlotScape.AnimPlotTimeSteps(s, "sugar", scapeStates)   
PlotScape.AnimPlotTimeSteps(s, "pollution", scapeStates)      
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
def groupAgentsByCultureTags(agents: List[Agent], threshold: float = 1) -> Dict[int, int]:
    # define hash table to store cluster tags
    # Dict of group index to list of agents ids
    #agent_groups: Dict[int, List[int]] = {}
    # Dict of agents ids to groups
    agentid_to_groups: Dict[int, int] = {}
    
    agentid_to_agent: Dict[int, Agent] = {}
    
    for agent in agents:
        agentid_to_agent[agent.id] = agent
        
        
    # select first tag as first cluster
    cluster_tagAgent = agentid_to_agent[agents[0].id]
    del agentid_to_agent[agents[0].id]
    
    clusterIndex = 0

    while len(agentid_to_agent) > 0:
        agentid_to_groups[cluster_tagAgent.id] = clusterIndex
        
        newClusterTagAgent = None
        agent_remove_buffer = []
        # loop through all tags and compare to cluster tag, check if cultural similarity is less than threshold
        for _, agent in agentid_to_agent.items():
            
            similarity = CulturalSimilarityFunction(cluster_tagAgent.GetProperty("culture_tag"), agent.GetProperty("culture_tag"))
            if similarity < threshold:
                # Not in cluster
                newClusterTagAgent = agent
                #print("New cluster tag agent ", newClusterTagAgent.id, " with similarity ", similarity)
            else:
                # In cluster
                #if clusterIndex not in agent_groups:
                #    agent_groups[clusterIndex] = []
                
                #agent_groups[clusterIndex].append(agent.id)
                agent_remove_buffer.append(agent.id)
                agentid_to_groups[agent.id] = clusterIndex
                #print("Agent ", agents[i].id, " is in cluster ", clusterIndex)
             
        for agentid in agent_remove_buffer:
            del agentid_to_agent[agentid]
               
        clusterIndex += 1   
        if  newClusterTagAgent is not None:
            del agentid_to_agent[newClusterTagAgent.id]
        cluster_tagAgent = newClusterTagAgent
        
        
        #print(len(agent_groups), len(agents))
        
    #print("Clustered ", len(agentid_to_groups), " agents into ", clusterIndex, " groups")
    return agentid_to_groups


#PlotScape.AnimPlotAgentAttributeTimeSteps(s, saveStates, agentStates, colorByVision)
#PlotScape.AnimPlotAgentAttributeTimeSteps(s, scapeStates, agentStates, colorByTribe)
#PlotScape.PrintAgentPropertyMean(s, range(0, SIM_TIME), ["vision", "metabolism"], agentStates)
PlotScape.AnimPlotAgentGrouping(s, lambda x : groupAgentsByCultureTags(x, 0.7), agentStates, scapeStates)
plt.show()