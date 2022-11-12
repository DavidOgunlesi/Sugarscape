from core.imports import *
from core.scape import Scape
from core.agent import Agent
from core.attribute import Attribute

class Sugarscape:
    
    def __init__(self, width: int, height:int = None):
        self._scapes : Dict[str, Scape] = {} # Dict of attribute names and their respective scape maps
        self._scapeRules: List[Tuple(str, Callable, Callable, Callable)] = []
        self._agents: List[Agent] = []
        self._newAgentCount:int = 0
        self._defaultProps: Dict[str,float] = {}
        self._saveStates: Tuple(List[Dict[str, Scape]], List[List[Agent]]) = ([],[])
        self.rules: List[(Callable, Callable)] = []
        self._agentDeleteBuffer:List[Agent]  = []
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
           
    def AddAgents(self, agentCount: int):
        for _ in range(min(agentCount, self.width * self.height)):
            id = len(self._agents)
            self.GetScape("agents").SetRandomUnit(id, True)
            agent = Agent(id, self.GetScape("agents"))
            self._agents.append(agent)
            
    def _ReplaceAgents(self, agentCount: int):
        for _ in range(min(agentCount, self.width * self.height)):
            id = len(self._agents)
            self.GetScape("agents").SetRandomUnit(id, True)
            agent = Agent(id, self.GetScape("agents"))
            for init, _ in self.rules:
                # init agent behaviour
                init(self, agent)
            self._agents.append(agent)
    
    def KillAgent(self, agent:Agent):
        agent.SetProperty("dead", 1)
        if agent not in self._agentDeleteBuffer:
            self._agentDeleteBuffer.append(agent)
            
    def AddNewAgent(self):
        self._newAgentCount += 1
        
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
        
    def RunSimulation(self, epochCount: int = 0):
        
        for scapeName in self._scapes:
            self._scapes[scapeName].SaveInitialState()
        
        # Init agents
        for init, _ in self.rules:
            # Run agent behaviour
            for agent in self._agents:
                init(self, agent)
        
        # init scapes
        for _, init, _, _  in self._scapeRules:
            scape = self.GetScape(scapeName)
            init(self, scape)
        
        for epoch in range(max(epochCount, 0)):
            # Create replacements
            #print("REPCOUNT:", self._newAgentCount)
            self._ReplaceAgents(self._newAgentCount)
            self._newAgentCount = 0
            #print("TOTALPOP:", len(self._agents), self.GetScape("agents").FilledValueCount())
            # save state
            if self.saveEpochs and (epoch) % (self.epochSkip+1) == 0:
                self._saveStates[0].append(copy.deepcopy(self._scapes))
                self._saveStates[1].append(copy.deepcopy(self._agents))
                #print(self._saveStates[0][len(self._saveStates[0])-1]["agents"]._scape[0:10])
                
            # Update scape maps
            for scapeName, _, step, cellstep  in self._scapeRules:
                scape = self.GetScape(scapeName)
                step(epoch, self, scape)
                for i in range(len(scape._scape)):
                    x, y = scape.IndexToCoordinates(i)
                    cellstep(self, scape, x, y, scape._scape[i])
                    
                
            
            # TODO: Optimise this step with Cython + threading
            for _, rule in self.rules:
                # Run agent behaviour
                for agent in self._agents:
                    rule(self, agent)
            
            #print("DEATHCOUNT:", len(self._agentDeleteBuffer))
            for agent in self._agentDeleteBuffer:
                self._agents.remove(agent)
                
            self._agentDeleteBuffer.clear()
            
            #Update agent positions
            self.GetScape("agents").Clear()
            for agent in self._agents:
                self.GetScape("agents").SetValue(agent.x, agent.y, agent.id)
    
    def GetScapeSaveStates(self):
        return self._saveStates[0]
    
    def GetAgentSaveStates(self):
        return self._saveStates[1]
      