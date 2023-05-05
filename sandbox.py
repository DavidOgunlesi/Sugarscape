from __future__ import annotations
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

#test = culstertags([[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1,0,0],[1,1,1,1,1,1,1,0,0,0],[1,1,1,1,1,1,0,0,0,0],[1,1,1,1,1,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])

#print(test)

# spiceWealth = 2
# sugarWealth = 2
# spiceMetabolicRate = 1
# sugarMetabolicRate = 1
# metabolicSum = spiceMetabolicRate + sugarMetabolicRate
# print((spiceWealth**(spiceMetabolicRate/metabolicSum)) * (sugarWealth**(sugarMetabolicRate/metabolicSum)))

# import pyEdgeworthBox as eb

# spiceWealth = [4,2]
# sugarWealth = [2,6]
# spiceMetabolicRate = [1.4,1.6]
# sugarMetabolicRate = [1.2,1.8]
# metabolicSum = [spiceMetabolicRate[0] + sugarMetabolicRate[0], spiceMetabolicRate[1] + sugarMetabolicRate[1]]
# utilFunc1 = lambda x,y: x**(sugarMetabolicRate[0]/metabolicSum[0])*y**(spiceMetabolicRate[0]/metabolicSum[0])
# utilFunc2 = lambda x,y: x**(sugarMetabolicRate[1]/metabolicSum[1])*y**(spiceMetabolicRate[1]/metabolicSum[1])
# EB=eb.EdgeBox(  u1 = utilFunc2
#               , u2 = utilFunc1
#               , IE1 = [sugarWealth[0],spiceWealth[0]]
#               , IE2 = [sugarWealth[1],spiceWealth[1]])
# EB.plot()
# input()

#TODO: Make function to average all trades and then plot
import numpy as np

training_set_inputs = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
training_set_outputs = np.array([[0, 1, 1, 0]]).T



class NeuralNetwork():
    def __init__(self, layers: List[int]):
        
        l = Layer(layers[0])
        for i in range(1, len(layers)):
            l.ConnectLayer(Layer(layers[i]))
            
        self.networks = l

    def ForwardPropagate(self, inputs: np.array):
        curr_layer = self.networks
        activations = curr_layer.CalculateActivations(inputs)
        
        curr_layer = curr_layer.forwardLayer
        
        while curr_layer is not None:
            activations = curr_layer.CalculateActivations(activations)
            curr_layer = curr_layer.forwardLayer
            
        return activations
    
    def Train(self, inputs: np.array, desired_outputs: np.array):
        activations = self.ForwardPropagate(inputs)
        print(activations)

class Layer():
    
    def __init__(self, node_count: int):
        np.random.seed(1)
        
        self.node_count = node_count
        self.biases = np.random.random((node_count, 1))
        
        self.synaptic_weights = None
            
        #print(self.synaptic_weights)
        #print(self.biases)
        
    def ConnectLayer(self, output_layer: Layer):
        self.forwardLayer = output_layer
        self.synaptic_weights = np.random.random((self.node_count, output_layer.node_count))
    
    def CalculateActivations(self, inputs: np.array) -> np.array:
        return np.dot(self.synaptic_weights, inputs) + self.biases
        
        
#neuralnet = NeuralNetwork([3,16,3])
##inputs = np.array([1,1,1])
#print(neuralnet.Train(inputs, None))

#x = np.array([-1, -1, -1, 4, 5, 5, -1, -1,-1, -1, 2, 65])
#print(np.count_nonzero(x == -1))

#read csc column into list
# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv('casestudy/Japan-2022.csv')
# # remove last 3 rows from df
# df = df[:-3]
# # keep first 3 columns
# df = df.iloc[:, 0:3]

# y = df['Age']
# x1 = df['M'].apply(lambda x: float(x))
# x2 = df['F'].apply(lambda x: -float(x))
# print(x1, x2)
# fig = plt.figure()
# # Create a horizontal bar plot
# ax = fig.add_subplot(111)

# # Plot the Male bars
# ax.barh(y, x1, 0.9, label='Male')

# # Plot the Female bars
# ax.barh(y, x2, 0.9, label='Female')

# # Set the y-axis label
# ax.set_ylabel('Age')

# # Set the x-axis label
# ax.set_xlabel(f"Population")

# # Set the x-axis tick values and labels
# t1 = 4000000.0
# t2 = 8000000.0
# ax.set_xticks([-t2, -t1, 0, t1, t2])
# ax.set_xticklabels([t2, t1, '0', t1, t2])

# # Set the title
# ax.set_title("Japan Population Pyramid 2022", fontsize=16)

# # Set the legend
# ax.legend()

# plt.show()
import random

average_life_span = 85.03

# Define the range around the average life span
range_min = average_life_span - 5  # 5 years below the average
range_max = average_life_span + 5  # 5 years above the average

# Generate a random age within the defined range
random_age = random.uniform(range_min, range_max)

print(random_age)