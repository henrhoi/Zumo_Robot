__author__  = "Kristoffer Gjerde"
from random import uniform


#Implement haltrequest?

class Arbitrator:


    def __init__(self,bbcon,storkastisk):
        self.bbcon = bbcon
        self.storkastisk = storkastisk


    def choose_action(self):
        if self.storkastisk: return self.storkastisk_valg()
        else: return self.deterministisk_valg()

    #Velger den med størst prioritet
    def deterministisk_valg(self):
        if self.bbcon.active_behaviors == []:
            return ["B",1,2]
        sorted_behaviors = sorted(self.bbcon.active_behaviors,key= lambda x:x.weight)
        return sorted_behaviors[-1].motor_recommendations


    #Velger en behavior storkastisk, lager intervall, velger random.
    def storkastisk_valg(self):
        if self.bbcon.active_behaviors == []:
            return ["B",1,2]
        liste = [behavior.weight for behavior in self.bbcon.active_behaviors]
        start = 0
        ranged = []
        for weight in liste:
            weight = weight + start
            ranged.append(set(x / 1000 for x in range(int(start * 1000), int(weight * 1000))))
            start = weight
        random = round(uniform(0, sum(liste) - 0.001), 2)

        res = 0
        for x in range(len(ranged)):
            if random in ranged[x]:
                res = x
        return self.bbcon.active_behaviors[res].motor_recommendations




