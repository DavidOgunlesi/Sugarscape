from __future__ import annotations
import random
import threading
import matplotlib.pyplot as plt
from core.lib import *
import time

s = Sugarscape(100)
s.AddAgents(500)
s.CreateScape(Attribute("sugar", 0, 100))
s.CreateScape(Attribute("pollution", 0, 100))
#s.GetScape("sugar").FillWithRandomValues(0, 100, True)

s.GetScape("sugar").FillWithPerlinNoise(octaves=1)
s.GetScape("sugar").Normalise(True)
s.GetScape("pollution").FillWithPerlinNoise(octaves=1)
s.GetScape("pollution").Normalise(True)
#s.GetScape("sugar").DefaultValuesByCutOff(70,False)

#import rules.scape.rule_growback as growback
import rules.scape.rule_seasonal_growback as growback 
s.AddScapeRule("sugar", growback.Init, growback.Step, growback.CellStep)
 
import rules.scape.rule_pollution_diffusion as pol 
s.AddScapeRule("pollution", pol.Init, pol.Step, pol.CellStep)
 
import rules.agent.rule0_metabolism as rule0
s.AddAgentRule(rule0.Init, rule0.Step)

import rules.agent.rule1_movement as rule1
s.AddAgentRule(rule1.Init, rule1.StepPollutionModified)

import rules.agent.rule2_agent_replacement as rule2
s.AddAgentRule(rule2.Init, rule2.Step)

import rules.agent.rule3_pollution_formation as rule3
s.AddAgentRule(rule3.Init, rule3.Step)

s.SetHyperParameter("min_metabolism", 10)
s.SetHyperParameter("max_metabolism", 50)
s.SetHyperParameter("max_vision", 4)
s.SetHyperParameter("initial_endowment", 0)
s.SetHyperParameter("min_life_span", 7)
s.SetHyperParameter("max_life_span", 10)
s.SetHyperParameter("season_change_time", 5)
s.SetHyperParameter("sugar_growback_amount", 20)
s.SaveEpochs(True)
s.RunSimulation(30)
saveStates = s.GetScapeSaveStates()
agentStates = s.GetAgentSaveStates()

def Func(scape:Scape):
    return scape.FilledValueCount(True)

PlotScape.LinePlotAttributesOverTimeSteps(Func,s,"agents",saveStates, True)
       
PlotScape.AnimPlotTimeSteps(s, "agents", saveStates)    

PlotScape.AnimPlotTimeSteps(s, "sugar", saveStates)   
PlotScape.AnimPlotTimeSteps(s, "pollution", saveStates)      
#plots = ["sugar"]
#PlotScape.CurrentStatePlot(s, plots)

PlotScape.PrintAgentPropertyMean(range(0,30), ["vision", "metabolism"], agentStates)
plt.show()