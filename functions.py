from __future__ import annotations
from typing import List, Dict
from core.agent import Agent

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


def GetWelfare(agent: Agent, sugarAddition: float, spiceAddition: float) -> float:
    spiceWealth = agent.GetProperty("spice_wealth") + spiceAddition
    sugarWealth = agent.GetProperty("sugar_wealth") + sugarAddition
    spiceMetabolicRate = agent.GetProperty("spice_metabolism")
    sugarMetabolicRate = agent.GetProperty("sugar_metabolism")
    metabolicSum = spiceMetabolicRate + sugarMetabolicRate
    return (spiceWealth**(spiceMetabolicRate/metabolicSum)) * (sugarWealth**(sugarMetabolicRate/metabolicSum))

# use custom algo to cluster the tags into distinct groups based on cultural similarity threshold
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
