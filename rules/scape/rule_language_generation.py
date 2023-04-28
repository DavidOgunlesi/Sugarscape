from core.scape import Scape
from core.sugarscape import Sugarscape

def Init(sugarscape:Sugarscape, scape:Scape):
    # Generate languages
    for i in range(sugarscape.GetHyperParameter("initial_language_count")):
        # Generate random words
        for j in range(sugarscape.GetHyperParameter("initial_word_count")):
            pass

def Step(epoch: int, sugarscape:Sugarscape, scape:Scape):
    pass

def CellStep(sugarscape:Sugarscape, scape:Scape, x, y, value: float):
    pass
