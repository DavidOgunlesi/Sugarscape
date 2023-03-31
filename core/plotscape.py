from core.imports import *
from core.scape import Scape
from core.sugarscape import Sugarscape
from core.agent import Agent
class PlotScape():
    
    ########################################
    # NORMAL PLOT
    ########################################
    @classmethod
    def CurrentStatePlot(self,sugarscape:Sugarscape, plots: List[str]):
        self.fig = plt.figure()
        self.val = 0
        PlotScape.UpdatePlot(sugarscape, plots)
        self.fig.canvas.mpl_connect('button_press_event', lambda event: PlotScape.UpdatePlot(sugarscape, plots))
    
    @classmethod
    def UpdatePlot(self, sugarscape:Sugarscape, plots: List[str]):
        self.fig.clear()
        plt.clf()
        self.val += 1
        self.val %= len(plots)
        scape = sugarscape.GetScape(plots[self.val])
        self.fig.add_subplot(111)
        plt.title(f"SCAPE: {plots[self.val]}")
        scape.Plot(sugarscape.width, sugarscape.height)
        plt.draw()
      
    ########################################
    # AGENT ATTRIBUTE TIME VISUAL PLOT
    ########################################
    
    @classmethod
    def AnimPlotAgentGrouping(self ,sugarscape:Sugarscape, groupingFunc: Callable, agentTimesteps: List[List[Agent]], scapeTimesteps: List[Scape], ):
        agentTimesteps = copy.deepcopy(agentTimesteps)
        x = lambda scape, epoch : PlotScape.NormaliseScapeByAgentGrouping(agentTimesteps, epoch , scape, groupingFunc)
        PlotScape.AnimPlotTimeSteps(sugarscape, "agents", scapeTimesteps, x)
    
    @classmethod
    def AnimPlotAgentAttributeTimeSteps(self, 
        sugarscape:Sugarscape, 
        scapeTimesteps: List[Scape], 
        agentTimesteps: List[List[Agent]], 
        colorFunc:Callable[[Agent], int] = None
        ):
        agentTimesteps = copy.deepcopy(agentTimesteps)
        
        x = lambda scape, epoch : PlotScape.NormaliseScapeByAgentAttribute(agentTimesteps, epoch , scape, colorFunc)
        PlotScape.AnimPlotTimeSteps(sugarscape, "agents", scapeTimesteps, x)
        
    @classmethod 
    def NormaliseScapeByAgentGrouping(self, agentTimesteps: List[List[Agent]], timestep: int, scape:Scape, groupingFunc:Callable):
        scape.NormaliseOnPlot(False)
        # Set id to color based of function
        groups = groupingFunc(agentTimesteps[timestep])
        for agent in agentTimesteps[timestep]:
            if agent.id in groups:
                colorID = groups[agent.id] + 1
                #print(colorID)
                scape.SetValue(agent.x, agent.y, colorID)
            else:
                scape.SetDefault(agent.x, agent.y)
    
    @classmethod 
    def NormaliseScapeByAgentAttribute(self, agentTimesteps: List[List[Agent]], timestep: int, scape:Scape, colorAgentFuc:Callable):
        scape.NormaliseOnPlot(False)
        # Set id to color based of function
        for agent in agentTimesteps[timestep]:
            colorID = colorAgentFuc(agent)
            scape.SetValue(agent.x, agent.y, colorID)
        
        
    ########################################
    # TIME VISUAL PLOT
    ########################################
    @classmethod
    def AnimPlotTimeSteps(self, sugarscape:Sugarscape, plot: str, scapeTimesteps: List[Scape], func:Callable = None):
        #sugarscape = copy.deepcopy(sugarscape)
        #scapeTimesteps = copy.deepcopy(scapeTimesteps)
        
        self.fig = plt.figure()
        self.val = 0
        PlotScape.UpdateTimestep(sugarscape, plot, scapeTimesteps, func)
        #key_press_event <-  -> arrow keys TODO
        self.fig.canvas.mpl_connect('button_press_event', lambda event: PlotScape.UpdateTimestep(sugarscape, plot, scapeTimesteps, func))

    @classmethod   
    def UpdateTimestep(self, sugarscape:Sugarscape, plot: str, scapeTimesteps: List[Dict[str, Scape]], func:Callable):
        self.fig.clear()
        plt.clf()
        scape = scapeTimesteps[self.val][plot]
        
        # Func to do whatever we need to do to the scape before plotting
        if func != None:
            func(scape, self.val)
            
        self.fig.add_subplot(111)
        epochNum = self.val*max(sugarscape.epochSkip,1)
        plt.title(f"SCAPE: {plot} - EPOCH: {epochNum}")
        scape.Plot(sugarscape.width, sugarscape.height)
        self.val += 1
        self.val %= len(scapeTimesteps)
        plt.draw()
     
    @classmethod   
    def LinePlotAttributesOverTimeSteps(self, func:Callable, sugarscape:Sugarscape, attribName: str, scapeTimesteps: List[Dict[str, Scape]], normalise:bool = False):
        #sugarscape = copy.deepcopy(sugarscape)
        #scapeTimesteps = copy.deepcopy(scapeTimesteps)
        
        timesteps = []
        data = []
        for i in range(len(scapeTimesteps)):
            scape = scapeTimesteps[i][attribName]
            scape = copy.deepcopy(scape)
            if normalise:
                scape.Normalise(False)
            
            epochNum = i*max(sugarscape.epochSkip,1)
            result = func(scape, i)
            data.append(result)
            timesteps.append(epochNum)
        
        sns.set_theme(style="whitegrid")
        
        data = pd.DataFrame(data, timesteps)
        sns.lineplot(data=data, palette="tab10", linewidth=2.5, legend="brief")
        
    # TODO: Implement
    @classmethod  
    def SugarscapeComaparisonPlot(self):
        pass
    
    # TODO: Implement
    @classmethod  
    def Histogram(self):
        pass
    
    @classmethod  
    def PrintAgentPropertyMean(self, sugarscape:Sugarscape, epochs: List[int], attribNames:List[str], agentTimesteps: List[List[Agent]]):
        #sugarscape = copy.deepcopy(sugarscape)
        #agentTimesteps = copy.deepcopy(agentTimesteps)
        
        result = "MEAN: \n"
        epochsList = [] 
        for i in range(len(epochs)):
            if epochs[i] % max(sugarscape.epochSkip,1) == 0:
                epochsList.append(epochs[i]) 

        print("EPOCHS: ", epochsList)
        for epoch in range(len(agentTimesteps)):
            result += f"EPOCH: {epochsList[epoch]}\n"
            lst = agentTimesteps[epoch]
            if len(lst) == 0:
                result += "ALL AGENTS DEAD\n"
                break
            for attribName in attribNames:
                lst_mean = sum([i.GetProperty(attribName) for i in lst]) / len(lst)
                result += f"\t{attribName}: {lst_mean}\n"
        
        print(result)
            
        
            
 