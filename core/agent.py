from __future__ import annotations
from typing import TYPE_CHECKING
from core.imports import *
from core.scape import Scape

class Agent:
        def __init__(self, id, scape: Scape):
            self.scape = scape
            self.id = id
            self.x, self.y = self.GetPosition()
            self.properties: Dict[str, Any] = {}
        
        def GetProperty(self, property_name: str):
            if property_name in self.properties:
                return self.properties[property_name]
            else:
                return None
            
        def SetProperty(self, property_name: str, value):
            self.properties[property_name] = value
            
        def GetPosition(self):
            idx = self.scape.FindFirstValue(self.id)
            coords = self.scape.IndexToCoordinates(idx)
            return coords[0], coords[1]
        
        def MoveTo(self, x, y):
            if self.scape.IsInBounds(x, y) and self.scape.IsCellDefault(x, y):
                self.x, self.y = x, y
        