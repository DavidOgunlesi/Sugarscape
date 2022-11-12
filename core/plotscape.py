from core.imports import *
from core.scape import Scape
from core.sugarscape import Sugarscape
from core.agent import Agent
class PlotScape():
    
    @classmethod
    def CurrentStatePlot(self,sugarscape:Sugarscape, plots: List[str]):
        self.fig = plt.figure()
        self.val = 0
        PlotScape.UpdatePlot(sugarscape, plots)
        self.fig.canvas.mpl_connect('button_press_event', lambda event: PlotScape.UpdatePlot(sugarscape, plots))
    
    @classmethod
    def AnimPlotTimeSteps(self, sugarscape:Sugarscape, plot: str, scapeTimesteps: List[Scape]):
        self.fig = plt.figure()
        self.val = 0
        PlotScape.UpdateTimestep(sugarscape, plot, scapeTimesteps)
        #key_press_event <-  -> arrow keys TODO
        self.fig.canvas.mpl_connect('button_press_event', lambda event: PlotScape.UpdateTimestep(sugarscape, plot, scapeTimesteps))
    
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
     
    @classmethod   
    def UpdateTimestep(self, sugarscape:Sugarscape, plot: str, scapeTimesteps: List[Dict[str, Scape]]):
        self.fig.clear()
        plt.clf()
        scape = scapeTimesteps[self.val][plot]
        self.fig.add_subplot(111)
        epochNum = self.val*max(sugarscape.epochSkip,1)
        plt.title(f"SCAPE: {plot} - EPOCH: {epochNum}")
        scape.Plot(sugarscape.width, sugarscape.height)
        self.val += 1
        self.val %= len(scapeTimesteps)
        plt.draw()
     
    @classmethod   
    def LinePlotAttributesOverTimeSteps(self, func:Callable, sugarscape:Sugarscape, attribName: str, scapeTimesteps: List[Dict[str, Scape]], normalise:bool = False):
        timesteps = []
        data = []
        for i in range(len(scapeTimesteps)):
            scape = scapeTimesteps[i][attribName]
            scape = copy.deepcopy(scape)
            if normalise:
                scape.Normalise(False)
            
            epochNum = i*max(sugarscape.epochSkip,1)
            result = func(scape)
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
    def PrintAgentPropertyMean(self, epochs:int, attribNames:List[str], agentTimesteps: List[List[Agent]]):
        result = "MEAN: \n"
        for epoch in epochs:
            result += f"EPOCH: {epoch}\n"
            lst = agentTimesteps[epoch]
            for attribName in attribNames:
                lst_mean = sum([i.GetProperty(attribName) for i in lst]) / len(lst)
                result += f"\t{attribName}: {lst_mean}\n"
        
        print(result)
            
        
            
 