from __future__ import annotations
from typing import TYPE_CHECKING
from core.imports import *
from core.scape import Scape
import names

class Agent:
        def __init__(self, id, scape: Scape):
            self.scape: Scape = scape
            self.id: int = id
            self.x, self.y = self.GetPosition()
            self.properties: Dict[str, Any] = {}
            self.SetProperty("name", names.get_full_name())
            self.cachedNeighbours: List[int] = []
        
        def GetProperty(self, property_name: str):
            if property_name in self.properties:
                return self.properties[property_name]
            else:
                return None
            
        def SetProperty(self, property_name: str, value):
            self.properties[property_name] = value

        def ModifyProperty(self, property_name: str, value):
            self.properties[property_name] += value
            
        def GetAllProperties(self, mask: List[str] = None):
            if mask is None:
                return self.properties
            else:
                return {k: v for k, v in self.properties.items() if k in mask}
            
        def GetPosition(self):
            idx = self.scape.FindFirstValue(self.id)
            coords = self.scape.IndexToCoordinates(idx)
            return coords[0], coords[1]
        
        def MoveTo(self, x, y):
            if self.scape.IsInBounds(x, y) and self.scape.IsCellDefault(x, y):
                self.x, self.y = x, y
        
        def OnEndStep(self):
            self.cachedNeighbours.clear()
             
        def GetAgentNeighbours(self) -> List[int]:
            
            if len(self.cachedNeighbours) > 0:
                return self.cachedNeighbours
            
            visionVectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            neighbors = []
            for i in range(1, self.GetProperty("vision")+1):
                for v in visionVectors:
                    x = self.x + (v[0] * i)
                    y = self.y + (v[1] * i)
                    
                    if not self.scape.IsInBounds(x, y):
                        continue
                    
                    agentNeigbour = self.scape.GetValue(x, y)
                    
                    if agentNeigbour != None:
                        neighbors.append(agentNeigbour) 
                        
            self.cachedNeighbours = neighbors
            return neighbors
        
        def DoOnTileNeighbours(self, func: Callable[[int,int], None]):
            
            visionVectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            for i in range(1, self.GetProperty("vision")+1):
                for v in visionVectors:
                    x = self.x + (v[0] * i)
                    y = self.y + (v[1] * i)
                    
                    if not self.scape.IsInBounds(x, y):
                        continue
                    
                    func(x, y)
                    
        # Function to create the
        # random binary string
        def rand_key(self, length, seed=0):
        
            # Variable to store the
            # string
            key1 = []
        
            # Loop to find the string
            # of desired length
            for _ in range(length):
                
                # randint function to generate
                # 0, 1 randomly and converting
                # the result into str
                random.seed(seed)
                temp = random.randint(0, 1)
        
                # Concatenation the random 0, 1
                # to the final result
                key1.append(temp)
                
            return(key1)
                    
                    
        