from core.imports import *
from core.scape import Scape
from core.agent import Agent
from core.attribute import Attribute
from alive_progress import alive_bar
from core.rules import ScapeRule, AgentRule
import tracemalloc
import time

class Sugarscape:
    
    def __init__(self, width: int, height:int = None):
        self._scapes : Dict[str, Scape] = {} # Dict of attribute names and their respective scape maps
        self._scapeRules: List[ScapeRule] = []
        self._agents: Dict[int, Agent] = {} # Dict of agent ids and their respective agents
        self._totalAgentCount = 0
        self._newAgentCount:int = 0
        self._defaultProps: Dict[str, float] = {}
        self._defaultFuncProps: Dict[str, Callable] = {}
        self._statsProps: Dict[str, float] = {}
        self._saveStates: Tuple(List[Dict[str, Scape]], List[List[Agent]]) = ([],[])
        self.rules: List[AgentRule] = []
        self._agentCreateBuffer: Dict[str, Agent] = {}
        self._agentDeleteBuffer:List[int]  = []
        self.saveEpochs = False
        self.epochSkip = 0
        self.agentScape = None
        self.start_time = time.time()
        self.init = False
        if height == None:
            height = width
        
        self.width = width
        self.height = height
        
        if width < 0:
            logging.exception("Dimensions of sugarscape cannot be negative")
            
        self.agentScape = self.CreateScape(Attribute("agents", defaultValue=-1))
        self.GetScape("agents").NormaliseOnPlot(True)
               
    def CreateScape(self, scapeAttribute: Attribute) -> Scape:
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
        return scape
       
    def GetScape(self, attribName: str) -> Scape:
        if self._scapes[attribName]: 
            return self._scapes[attribName]
        else:
            logging.exception("Scape Attribute does not exist")
            return None
    
    def BirthNewAgentAtPos(self, x:int, y:int):
        id = self._totalAgentCount
        self.agentScape.SetValue(x, y, id)
        agent = Agent(id, self.agentScape)
        self._agentCreateBuffer[id] = agent
        self._totalAgentCount += 1
        return agent
           
    def AddAgents(self, agentCount: int):
        with alive_bar(max(agentCount, 0)) as bar:
            for _ in range(min(agentCount, self.width * self.height)):
                id = self._totalAgentCount
                self.agentScape.SetRandomUnit(id, True)
                agent = Agent(id, self.agentScape)
                self._agents[id] = agent
                self._totalAgentCount += 1
                bar.text(f"Adding agent with id: {id} at {agent.x}, {agent.y}")
                bar()

    def GetAllAgents(self):
        return self._agents.values()
    
    def SplitAgentsByPredicate(self, agents: List[Agent], predicate:Callable[[Agent], bool]) -> Tuple[List[Agent], List[Agent]]:
        return (list(filter(predicate, agents)), list(filter(lambda x: not predicate(x), agents)))
    
    def SplitAgentsIntoPercentageGroups(self, agents: List[Agent], total, percentages:List[float]) -> List[List[Agent]]:
        #print("total", total)
        groups = []
        for i in range(len(percentages)):
            count = int(percentages[i] * total)
            #print("count", count, total)
            count = min(count, len(agents))
            groups.append(agents[:count])
            agents = agents[count:]
        
        #print(len(agents))
        return groups

    def _ReplaceAgents(self, agentCount: int):
        for _ in range(min(agentCount, self.width * self.height)):
            id = self._totalAgentCount
            self.agentScape.SetRandomUnit(id, True)
            agent = Agent(id, self.agentScape)
            for agentRule in self.rules:
                # init agent behaviour
                agentRule.init(self, agent)
            self._agents[id] = agent
            self._totalAgentCount += 1
    
    def _BirthAgents(self):
        for id in self._agentCreateBuffer:
            agent = self._agentCreateBuffer[id]
            self._agents[agent.id] = agent
            #print("BIRTH: ", agent.GetProperty("culture_tag"))
            for agentRule in self.rules:
                # init agent behaviour
                agentRule.init(self, agent)
        self._agentCreateBuffer.clear()
    
    def KillAgent(self, agent:Agent, cause:str = "unspecified"):
        agent.SetProperty("dead", 1)
        if agent.id not in self._agentDeleteBuffer:
            self._agentDeleteBuffer.append(agent.id)
        
        self.AddStats("deaths", 1)
        self.AddStats("deaths_" + cause, 1)
            
    def AddNewAgent(self):
        self._newAgentCount += 1
      
    def GetAgentAtPosition(self, x:int, y:int):
        id = self.agentScape.GetValue(x,y)
        if id != -1:
            if id not in self._agents:
                # Agent is in the buffer (probably bc they were just born) so we can ingnore them
                return self._agentCreateBuffer[id]
            
            return self._agents[id]
        
        return None
    
    def GetAgentFromId(self, id:int):
        if id in self._agents:
            return self._agents[id]
        return None
        
    def AddAgentRule(self, init:Callable, rule:Callable):    
        self.rules.append(AgentRule(init,rule))    
    
    def AddScapeRule(self, scapeName:str, init:Callable, step:Callable, cellstep:Callable):
        self._scapeRules.append(ScapeRule(scapeName, init, step, cellstep))
    
    def SetHyperParameter(self, attribName:str , value:float):
        self._defaultProps[attribName] = value 
    
    def SetHyperFunction(self, attribName:str , value:Callable):
        self._defaultFuncProps[attribName] = value
        
    def SetStats(self, attribName:str , value:float):
        self._statsProps[attribName] = value

    def GetHyperParameter(self, attribName:str, defaultValue:float = 0):
        if attribName in self._defaultProps:
            return self._defaultProps[attribName]
        print(f"Hyperparameter {attribName} not present on sugarscape, defaulting to {defaultValue}")
        return defaultValue

    def GetHyperFunction(self, attribName:str):
        if attribName in self._defaultFuncProps:
            return self._defaultFuncProps[attribName]
        print(f"HyperFunction {attribName} not present on sugarscape.")
        return lambda x: 0
    
    def GetStats(self, attribName:str, defaultValue:float = 0, verbose:bool = False):
        if attribName in self._statsProps:
            return self._statsProps[attribName]
        
        if verbose:
            print(f"Stats {attribName} not present on sugarscape, defaulting to {defaultValue}")
        return defaultValue
    
    def AddStats(self, attribName:str, value:float):
        if attribName in self._statsProps:
            self._statsProps[attribName] += value
        else:
            self._statsProps[attribName] = value
        
    def PrintStats(self):
        print("Stats: ")
        for key, value in self._statsProps.items():
            print(f"{key}: {value}")

    def SaveEpochs(self, value:bool, epochSkip:int = 0):
        self.saveEpochs = value 
        self.epochSkip = epochSkip
      
    def InitialiseSimulation(self):
        if self.init:
            return
        # starting the monitoring
        tracemalloc.start()
        self.start_time = time.time()
        for scapeName in self._scapes:
            self._scapes[scapeName].SaveInitialState()
        
        # Init agents
        for agentRule in self.rules:
            # Run agent behaviour
            for id in self._agents:
                agentRule.init(self, self._agents[id])
        
        # init scapes
        for scapeRule in self._scapeRules:
            scape = self.GetScape(scapeName)
            scapeRule.init(self, scape)
        
        self.init = True
        
    def RunSimulation(self, epochCount: int = 0):
        
        self.InitialiseSimulation()
         
        with alive_bar(max(epochCount, 0)) as bar:
            for epoch in range(max(epochCount, 0)):
                # If all agents are dead, we can stop the simulation
                if len(self._agents) == 0:
                    #print("ALL AGENTS DEAD")
                    break
                # Create replacements
                bar.text(f'Creating {self._newAgentCount} new agents')
                #self._ReplaceAgents(self._newAgentCount)
                #print("REPLACING AGENTS")
                self._BirthAgents()
                
                self._newAgentCount = 0

                #print(f"Epoch {epoch} started, scape: {self.agentScape.FilledValueCount(False)}")
                # save state
                bar.text(f'Saving simulation state')
                if self.saveEpochs and (epoch) % (self.epochSkip+1) == 0:
                    self._saveStates[0].append(copy.deepcopy(self._scapes))
                    self._saveStates[1].append(copy.deepcopy(list(self._agents.values())))
                    
                # bar.text(f'Updating scapes')
                # Update scape maps
                # TODO: Optimise this step with Cython + threading
                # SLOWEST STEP
                #print("UPDATING SCAPES")
                for scapeRule in self._scapeRules:
                    scape = self.GetScape(scapeRule.scapeName)
                    scape.SaveSnapshot()
                    scapeRule.step(epoch, self, scape)
                    for i in range(len(scape._scape)):
                        x, y = scape.IndexToCoordinates(i)
                        scapeRule.cellstep(self, scape, x, y, scape._scape[i])
                        
                # bar.text(f'Updating agents')
                # TODO: Optimise this step with Cython + threading
                #print("UPDATING AGENTS")
                for agentRule in self.rules:
                    # Run agent behaviour
                    for id in self._agents:
                        agentRule.rule(self, self._agents[id])
                
                
                #print("KILLING AGENTS")
                bar.text(f'Killing {len(self._agentDeleteBuffer)} agents')
                for id in self._agentDeleteBuffer:
                    if id in self._agents:
                        del self._agents[id]
                    
                self._agentDeleteBuffer.clear()
                
                bar.text(f'Updating agent positions')
                #Update agent positions
                # TODO: Optimise this step with Cython + threading
                #print("UPDATING AGENT POSITIONS")
                self.agentScape.Clear()
                #print(f"cleared scape: {self.agentScape.FilledValueCount(False)}")
                #print(f"agents: {len(self._agents)}")
                for id in self._agents:
                    agent = self._agents[id]
                    agent.OnEndStep()
                    self.agentScape.SetValue(agent.x, agent.y, agent.id)
                #print(bi, ci)
                
                #print(f"after agent on scape: {self.agentScape.FilledValueCount(False)} {self.agentScape._scape[0:9999]}")
                bar.text(f'Epoch {epoch} complete')  
                # sleep(0.01)  
                # Increment progress bar
                #print population
                #print(f"Epoch {epoch} complete, population: {len(self._agents)}")
                bar()
        
        print(f"--- Ran in {((time.time() - self.start_time)*1000)} ms ---")
        # displaying the memory
        print(f'Memory used: {tracemalloc.get_traced_memory()}')
        # stopping the library
        tracemalloc.stop()
    
    def GetScapeSaveStates(self):
        return self._saveStates[0]
    
    def GetAgentSaveStates(self):
        return self._saveStates[1]
      