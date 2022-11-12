from core.scape import Scape
from core.sugarscape import Sugarscape

def Init(sugarscape:Sugarscape, scape:Scape):
    pass

def Step(epoch: int, sugarscape:Sugarscape, scape:Scape):
    pass

def CellStep(sugarscape:Sugarscape, scape:Scape, x, y, value: float):
    vonNeumanPositions = [ (0, -1), (-1, 0), (1, 0), (0, 1)]
    
    # Calculate flux
    avg = 0
    count = 0
    for xx,yy in vonNeumanPositions:
        if scape.IsInBounds(xx,yy):
            avg += scape.GetValue(xx,yy)
            count += 1
    
    avg/=count
    scape.SetValue(x, y, avg)
