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
    def AnimPlotPopulationPyramid (self, title:str, agentTimesteps: List[List[Agent]]):
        self.fig = plt.figure()
        self.val = 0
        PlotScape.UpdatePopulationPyramid(title, agentTimesteps)
        self.fig.canvas.mpl_connect('button_press_event', lambda event: PlotScape.UpdatePopulationPyramid(title, agentTimesteps))

    @classmethod
    def UpdatePopulationPyramid(self, title:str, agentTimesteps: List[List[Agent]]):
        self.fig.clear()
        plt.clf()
        self.val += 1
        self.val %= len(agentTimesteps)
        agentTimestep = agentTimesteps[self.val]
        PlotScape.PlotPopulationPyramid(title, agentTimestep)
        plt.draw()


    @classmethod
    def PlotPopulationPyramid(self, title:str, agentTimestep: List[Agent]):

        def CountAgentAgentRange(agents, minage, maxage):
            count = 0
            for agent in agents:
                if agent.GetProperty("age") >= minage and agent.GetProperty("age") <= maxage:
                    count+=1
            return count
        
        df = pd.DataFrame(columns=['Age', 'M', 'F'])
        ages = [[100,104],[95,99],[90,94],[85,89], [80,84], [75,79], [70,74], [65,69], [60,64], [55,59], [50,54], [45,49], [40,44], [35,39], [30,34], [25,29], [20,24], [15,19], [10,14], [5,9], [0,4]]

        for age in ages:
            #df = pd.concat(df, {'Age': age[0], 'M': CountAgentAgentRange(agentTimestep, age[0], age[1]), 'F': CountAgentAgentRange(agentTimestep, age[0], age[1])}, ignore_index=True)
            df = pd.concat([df, pd.DataFrame.from_records([{'Age': age[0], 'M': CountAgentAgentRange(agentTimestep, age[0], age[1]), 'F': CountAgentAgentRange(agentTimestep, age[0], age[1])}])])
        
        y = df['Age']
        x1 = df['M']
        x2 = df['F'] * -1
        # Create a horizontal bar plot
        ax = self.fig.add_subplot(111)

        # Plot the Male bars
        ax.barh(y, x1, 5, label='Male', )

        # Plot the Female bars
        ax.barh(y, x2, 5, label='Female')

        # Set the y-axis label
        ax.set_ylabel('Age')

        # Set the x-axis label
        ax.set_xlabel(f"Agent Population \n Epoch {self.val}")

        # Set the x-axis tick values and labels
        t1 = int(len(agentTimestep)/16)
        t2 = int(len(agentTimestep)/8)
        ax.set_xticks([-t2, -t1, 0, t1, t2])
        ax.set_xticklabels([t2, t1, '0', t1, t2])

        # Set the title
        ax.set_title(title, fontsize=24)

        # Set the legend
        ax.legend()


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
    def LinePlotAttributesOverTimeSteps(self, func:Callable, sugarscape:Sugarscape, title:str ,attribName: str, scapeTimesteps: List[Dict[str, Scape]], normalise:bool = False):
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
        ax = sns.lineplot(data=data, palette="tab10", linewidth=2.5, legend="brief")
        ax.set_xlabel("epochs")
        ax.set_ylabel(attribName)
        plt.title(title)
        

    @classmethod   
    def LinePlotStatsOverTimeSteps(self, sugarscape:Sugarscape, title:str, ylabel:str, statName: str, statTimesteps: List[Dict[str, float]]):
        timesteps = []
        data = []
        for i in range(len(statTimesteps)):
            stats = statTimesteps[i]
            if statName not in stats:
                continue
            stat = stats[statName]
            epochNum = i*max(sugarscape.epochSkip,1)
            data.append(stat)
            timesteps.append(epochNum)
        
        sns.set_theme(style="whitegrid")
        
        data = pd.DataFrame(data, timesteps)
        ax = sns.lineplot(data=data, palette="tab10", linewidth=2.5, legend="brief")
        ax.set_xlabel("epochs")
        ax.set_ylabel(ylabel)
        plt.title(title)


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
            
        
            
 