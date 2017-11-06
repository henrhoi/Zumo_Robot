__author__  = "Kristoffer Gjerde"
from random import randint


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
        sorted_behaviors = sorted(self.bbcon.active_behaviors,key= lambda x:x.weight)
        return sorted_behaviors[-1].motor_recommendations


    #Velger en behavior storkastisk, lager intervall, velger random.
    def storkastisk_valg(self):
        liste = [behavior.weight for behavior in self.bbcon.active_behaviors]
        start = 0
        ranged = []
        for weight in liste:
            weight = 10 * weight + start
            ranged.append(range(int(start), int(weight)))
            start = int(weight)
        random = randint(0, ranged[-1][-1])

        res = 0
        for x in range(len(ranged)):
            if random in ranged[x]:
                res = x
        return self.bbcon.active_behaviors[res].motor_recommendations

ar = Arbitrator("xx",True)
ar.deterministisk_valg()



