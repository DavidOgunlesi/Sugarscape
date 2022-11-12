from core.scape import Scape
from core.sugarscape import Sugarscape

def Init(sugarscape:Sugarscape, scape:Scape):
    pass

def Step(epoch: int, sugarscape:Sugarscape, scape:Scape):
    pass

def CellStep(sugarscape:Sugarscape, scape:Scape, x, y, value: float):
    if value < scape.GetInitial(x, y):
        scape.SetValue(x, y, value +  sugarscape.GetHyperParameter("sugar_growback_amount", 0))

