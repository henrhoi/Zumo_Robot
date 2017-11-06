sjef  = "Kristoffer Gjerde"
from random import randint

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
        return sorted_behaviors[-1]


    #Velger en behavior storkastisk, lager intervall, velger random.
    def storkastisk_valg(self):
        active_behaviors = self.bbcon.active_behaviors
        list = [behavior.weight for behavior in active_behaviors]
        start = 0
        ranged = []
        for weight in list:
            weight = 10 * weight + start
            ranged.append(range(int(start), int(weight)))
            start = int(weight)
        random = randint(0, ranged[-1][-1])

        res = 0
        for x in range(len(ranged)):
            if random in ranged[x]:
                res = x
        return active_behaviors[res]

ar = Arbitrator("xx",True)
ar.deterministisk_valg()



