from core.scape import Scape
from core.sugarscape import Sugarscape

def Init(sugarscape:Sugarscape, scape:Scape):
    scape.SetProperty("season", "summer")

def Step(epoch: int, sugarscape:Sugarscape, scape:Scape):
    # switch season 0: summer, 1: Winter
    currSeason = scape.GetProperty("season")
    if epoch % sugarscape.GetHyperParameter("season_change_time", 5000) == 0:
        if currSeason == "summer":
            scape.SetProperty("season", "winter")
        else:
            scape.SetProperty("season", "summer")

def CellStep(sugarscape: Sugarscape, scape:Scape, x, y, value: float):
    tileInSeason = scape.GetProperty("season")
    
    # Split season into 2 equal regions
    if y < scape.height/2:
        if tileInSeason == "summer":
            tileInSeason = "winter"
        else:
            tileInSeason = "summer"
            
    if tileInSeason == "summer":
        growbackRate = 1
    else:
        growbackRate = 0.1
    if value < scape.GetInitial(x, y):
        scape.SetValue(x, y, value + sugarscape.GetHyperParameter("sugar_growback_amount", 0) * growbackRate)

