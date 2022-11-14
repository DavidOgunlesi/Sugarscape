from core.imports import *
from core.scape import Scape
from core.agent import Agent
from core.attribute import Attribute
from alive_progress import alive_bar
from time import sleep

class Sugarscape:
    
    def __init__(self, width: int, height:int = None):
        self._scapes : Dict[str, Scape] = {} # Dict of attribute names and their respective scape maps
        self._scapeRules: List[Tuple(str, Callable, Callable, Callable)] = []
        self._agents: Dict[int,Agent] = {} # Dict of agent ids and their respective agents
        self._totalAgentCount = 0
        self._newAgentCount:int = 0
        self._defaultProps: Dict[str,float] = {}
        self._saveStates: Tuple(List[Dict[str, Scape]], List[List[Agent]]) = ([],[])
        self.rules: List[(Callable, Callable)] = []
        self._agentCreateBuffer: Dict[str, Agent] = {}
        self._agentDeleteBuffer:List[int]  = []
        self.saveEpochs = False
        self.epochSkip = 0
        if height == None:
            height = width
        
        self.width = width
        self.height = height
        
        if width < 0:
            logging.exception("Dimensions of sugarscape cannot be negative")
            
        self.CreateScape(Attribute("agents", defaultValue=-1))
        self.GetScape("agents").NormaliseOnPlot(True)
               
    def CreateScape(self, scapeAttribute: Attribute):
        """
        Creates a scape of width x height units. A scape is a resource map is a 2D array of ScapeUnits.
        Each ScapeUnit represents a cell in the Sugarscape and can have multiple attributes.

        Args:
            width (int): Width of the scape
            height (int, optional): Hight of the sugarscape. Defaults to None.
        """
        
        if not scapeAttribute:
            logging.exception("Scape Attribute must be specified")
        
        scape = Scape(self.width, self.height, scapeAttribute)
        self._scapes[scapeAttribute.attribName] = scape 
       
    def GetScape(self, attribName: str) -> Scape:
        if self._scapes[attribName]: 
            return self._scapes[attribName]
        else:
            logging.exception("Scape Attribute does not exist")
            return None
    
    def BirthNewAgentAtPos(self, x:int, y:int):
        id = self._totalAgentCount
        self.GetScape("agents").SetValue(x, y, id)
        agent = Agent(id, self.GetScape("agents"))
        self._agentCreateBuffer[id] = agent
        self._totalAgentCount += 1
        return agent
           
    def AddAgents(self, agentCount: int):
        for _ in range(min(agentCount, self.width * self.height)):
            id = self._totalAgentCount
            self.GetScape("agents").SetRandomUnit(id, True)
            agent = Agent(id, self.GetScape("agents"))
            self._agents[id] = agent
            self._totalAgentCount += 1
            
    def _ReplaceAgents(self, agentCount: int):
        for _ in range(min(agentCount, self.width * self.height)):
            id = self._totalAgentCount
            self.GetScape("agents").SetRandomUnit(id, True)
            agent = Agent(id, self.GetScape("agents"))
            for init, _ in self.rules:
                # init agent behaviour
                init(self, agent)
            self._agents[id] = agent
            self._totalAgentCount += 1
    
    def _BirthAgents(self):
        for id in self._agentCreateBuffer:
            agent = self._agentCreateBuffer[id]
            self._agents[agent.id] = agent
            for init, _ in self.rules:
                # init agent behaviour
                init(self, agent)
        self._agentCreateBuffer.clear()
    
    def KillAgent(self, agent:Agent):
        agent.SetProperty("dead", 1)
        if agent.id not in self._agentDeleteBuffer:
            self._agentDeleteBuffer.append(agent.id)
            
    def AddNewAgent(self):
        self._newAgentCount += 1
      
    def GetAgentAtPosition(self, x:int, y:int):
        id = self.GetScape("agents").GetValue(x,y)
        if id != -1:
            if id not in self._agents:
                # Agent is in the buffer (probably bc they were just born) so we can ingnore them
                return self._agentCreateBuffer[id]
            
            return self._agents[id]
        
        return None
        
    def AddAgentRule(self, init:Callable ,rule:Callable):    
        self.rules.append((init,rule))    
    
    def AddScapeRule(self, scapeName:str, init:Callable, step:Callable, cellstep:Callable):
        self._scapeRules.append((scapeName, init, step, cellstep))
    
    def SetHyperParameter(self, attribName:str , value:float):
        self._defaultProps[attribName] = value 
    
    def GetHyperParameter(self, attribName:str, defaultValue:float = 0):
        if attribName in self._defaultProps:
            return self._defaultProps[attribName]
        print(f"Hyperparameter {attribName} not present on sugarscape, defaulting to {defaultValue}")
        return defaultValue
        
    def SaveEpochs(self, value:bool, epochSkip:int = 0):
        self.saveEpochs = value 
        self.epochSkip = epochSkip
      
    def __InitialiseSimulation(self):
        for scapeName in self._scapes:
            self._scapes[scapeName].SaveInitialState()
        
        # Init agents
        for init, _ in self.rules:
            # Run agent behaviour
            for id in self._agents:
                init(self, self._agents[id])
        
        # init scapes
        for _, init, _, _  in self._scapeRules:
            scape = self.GetScape(scapeName)
            init(self, scape)
        
    def RunSimulation(self, epochCount: int = 0):
        
        self.__InitialiseSimulation()
            
        with alive_bar(max(epochCount, 0)) as bar:
            for epoch in range(max(epochCount, 0)):
                # If all agents are dead, we can stop the simulation
                if len(self._agents) == 0:
                    print("ALL AGENTS DEAD")
                    break
                # Create replacements
                bar.text(f'Creating {self._newAgentCount} new agents')
                self._ReplaceAgents(self._newAgentCount)
                self._BirthAgents()
                
                self._newAgentCount = 0
                # save state
                bar.text(f'Saving simulation state')
                if self.saveEpochs and (epoch) % (self.epochSkip+1) == 0:
                    self._saveStates[0].append(copy.deepcopy(self._scapes))
                    self._saveStates[1].append(copy.deepcopy(list(self._agents.values())))
                    
                bar.text(f'Updating scapes')
                # Update scape maps
                for scapeName, _, step, cellstep  in self._scapeRules:
                    scape = self.GetScape(scapeName)
                    scape.SaveSnapshot()
                    step(epoch, self, scape)
                    for i in range(len(scape._scape)):
                        x, y = scape.IndexToCoordinates(i)
                        cellstep(self, scape, x, y, scape._scape[i])
                        
                bar.text(f'Updating agents')
                # TODO: Optimise this step with Cython + threading
                for _, rule in self.rules:
                    # Run agent behaviour
                    for id in self._agents:
                        rule(self, self._agents[id])
                
                
                bar.text(f'Killing {len(self._agentDeleteBuffer)} agents')
                for id in self._agentDeleteBuffer:
                    del self._agents[id]
                    
                self._agentDeleteBuffer.clear()
                
                bar.text(f'Updating agent positions')
                #Update agent positions
                self.GetScape("agents").Clear()
                for id in self._agents:
                    agent = self._agents[id]
                    self.GetScape("agents").SetValue(agent.x, agent.y, agent.id)
                bar.text(f'Epoch {epoch} complete')  
                sleep(0.01)  
                # Increment progress bar
                bar()
    
    def GetScapeSaveStates(self):
        return self._saveStates[0]
    
    def GetAgentSaveStates(self):
        return self._saveStates[1]
      