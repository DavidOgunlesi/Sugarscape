from typing import List

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

def culstertags(culturalTags: List[List[int]], threshold: float = 1):
    # define hash table to store cluster tags
    cluster_tags = {}
    # get number of clusters
    num_clusters = 0
    # select first tag as first cluster
    cluster_tag = culturalTags[0]
    clusterIndex = 0

    while len(culturalTags)-1 != len(cluster_tags):
        newClusterTag = None
        # loop through all tags and compare to cluster tag, check if cultural similarity is less than threshold
        for i in range(len(culturalTags[1:])):
            if str(culturalTags[i]) in cluster_tags:
                continue
            if CulturalSimilarityFunction(cluster_tag, culturalTags[i]) < threshold:
                # Not in cluster
                num_clusters += 1
                newClusterTag = culturalTags[i]
            else:
                # In cluster
                cluster_tags[str(culturalTags[i])] = clusterIndex
    
        cluster_tag = newClusterTag
        clusterIndex += 1
        print(len(cluster_tags), len(culturalTags) )
    return cluster_tags

test = culstertags([[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1,0,0],[1,1,1,1,1,1,1,0,0,0],[1,1,1,1,1,1,0,0,0,0],[1,1,1,1,1,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])

print(test)