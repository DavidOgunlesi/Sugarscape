from __future__ import annotations
from typing import Callable

class AgentRule:
    def __init__(self,init: Callable, step: Callable):
        self.init = init
        self.rule = step

class ScapeRule:
    def __init__(self, name: str, init: Callable, step: Callable, cellStep: Callable):
        self.scapeName = name
        self.init = init
        self.step = step
        self.cellstep = cellStep