import matplotlib.pyplot as plt
from core.lib import *
import functions

print(" Creating Sugarscape...")
s = Sugarscape(100)

print(" Adding Agents...")
s.AddAgents(7)

print(" Creating Scapes...")
s.CreateScape(Attribute("sugar", 0, 100))
s.CreateScape(Attribute("spice", 0, 100))
s.CreateScape(Attribute("pollution", 0, 100))

print(" Filling Scapes...")
s.GetScape("sugar").FillWithPerlinNoise(octaves=1) # 4
s.GetScape("sugar").Normalise(True)
s.GetScape("sugar").DefaultValuesByCutOff(70,False, True, 0.1)

s.GetScape("spice").FillWithPerlinNoise(octaves=2)
s.GetScape("spice").Normalise(True)
s.GetScape("spice").DefaultValuesByCutOff(70,False, True, 0.1)

print(" Adding Rules...")

import rules.scape.rule_growback as growback 
s.AddScapeRule("sugar", growback.Init, growback.Step, growback.CellStep)

import rules.scape.rule_seasonal_growback as seasonal_growback 
#s.AddScapeRule("sugar", seasonal_growback.Init, seasonal_growback.Step, seasonal_growback.CellStep)
 
import rules.scape.rule_diffusion as dif 
#s.AddScapeRule("pollution", dif.Init, dif.Step, dif.CellStep)
 
import rules.agent.rule0_metabolism as rule0
s.AddAgentRule(rule0.Init, rule0.SugarAndSpiceStep)

import rules.agent.rule1_movement as rule1
s.AddAgentRule(rule1.Init, rule1.StepPollutionAndWelfareModified)

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

import rules.agent.rule7_welfaretrade as rule7
s.AddAgentRule(rule7.Init, rule7.Step)

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


s.SetHyperFunction("cultural_similarity_function", functions.CulturalSimilarityFunction)

s.SetHyperFunction("welfare_function", functions.GetWelfare)

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
PlotScape.AnimPlotTimeSteps(s, "spice", scapeStates)   
PlotScape.AnimPlotTimeSteps(s, "pollution", scapeStates)      
#plots = ["sugar"]
#PlotScape.CurrentStatePlot(s, plots)

#PlotScape.AnimPlotAgentAttributeTimeSteps(s, saveStates, agentStates, functions.colorByVision)
#PlotScape.AnimPlotAgentAttributeTimeSteps(s, scapeStates, agentStates, functions.colorByTribe)
#PlotScape.PrintAgentPropertyMean(s, range(0, SIM_TIME), ["vision", "metabolism"], agentStates)
PlotScape.AnimPlotAgentGrouping(s, lambda x : functions.groupAgentsByCultureTags(x, 0.7), agentStates, scapeStates)
plt.show()