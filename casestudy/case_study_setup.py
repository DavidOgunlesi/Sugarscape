from core.lib import *
import csv

def SetUpAgentPopulation(sugarscape: Sugarscape, agent_count: int):
    ageData = []
    with open('casestudy/Japan-2022.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        #read csc column into list
        reader = list(reader)
        reader = reader[1:22]
        for row in reader:
            if row[6] != "":
                ageData.append({"male_percentage": float(row[7]), "female_percentage": float(row[8]), "minAge": int(row[9]), "maxAge": int(row[10])})

    #print(ageData)
    male_percentages = [ageData[i]["male_percentage"] for i in range(0, len(ageData))]
    female_percentages = [ageData[i]["female_percentage"] for i in range(0, len(ageData))]

    males, females = sugarscape.SplitAgentsByPredicate(sugarscape.GetAllAgents(), lambda agent: agent.GetProperty("sex") == "male")
    male_agentGroups = sugarscape.SplitAgentsIntoPercentageGroups(males, agent_count, male_percentages)
    female_agentGroups = sugarscape.SplitAgentsIntoPercentageGroups(females, agent_count, female_percentages)

    groupCatergories = [male_agentGroups, female_agentGroups]

    for groupCategory in groupCatergories:
        for group in groupCategory:
            minAge = int(ageData[groupCategory.index(group)]["minAge"])
            maxAge = int(ageData[groupCategory.index(group)]["maxAge"])
            #print(minAge, maxAge)
            for agent in group:
                age = random.randint(minAge, maxAge)
                agent.SetProperty("age", age)

    for agent in sugarscape.GetAllAgents():
        if agent.GetProperty("age") == 0:
            agent.SetProperty("age", random.randint(0, 100))
