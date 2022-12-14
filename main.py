from __future__ import annotations
import random
import threading
import matplotlib.pyplot as plt
from core.lib import *
import time

s = Sugarscape(100)
s.AddAgents(750)
s.CreateScape(Attribute("sugar", 0, 100))
s.CreateScape(Attribute("pollution", 0, 100))
#s.GetScape("sugar").FillWithRandomValues(0, 100, True)

s.GetScape("sugar").FillWithPerlinNoise(octaves=4)
s.GetScape("sugar").Normalise(True)
#s.GetScape("pollution").FillWithPerlinNoise(octaves=1)#
#s.GetScape("pollution").Normalise(True)
s.GetScape("sugar").DefaultValuesByCutOff(70,False, True, 0.5)
#import rules.scape.rule_growback as growback
import rules.scape.rule_seasonal_growback as growback 
s.AddScapeRule("sugar", growback.Init, growback.Step, growback.CellStep)
 
import rules.scape.rule_diffusion as dif 
s.AddScapeRule("pollution", dif.Init, dif.Step, dif.CellStep)
 
import rules.agent.rule0_metabolism as rule0
s.AddAgentRule(rule0.Init, rule0.Step)

import rules.agent.rule1_movement as rule1
s.AddAgentRule(rule1.Init, rule1.StepPollutionModified)

import rules.agent.rule2_agent_replacement as rule2
s.AddAgentRule(rule2.Init, rule2.Step)

import rules.agent.rule3_pollution_formation as rule3
s.AddAgentRule(rule3.Init, rule3.Step)

import rules.agent.rule4_sex as rule4
s.AddAgentRule(rule4.Init, rule4.Step)

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
s.SaveEpochs(True, 0)

SIM_TIME = 10
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
    

PlotScape.AnimPlotAgentAttributeTimeSteps(s, saveStates, agentStates, colorByVision)
PlotScape.PrintAgentPropertyMean(s, range(0, SIM_TIME), ["vision", "metabolism"], agentStates)
plt.show()