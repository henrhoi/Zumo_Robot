import time
from arbitrator import Arbitrator
from motob import Motob
__authors__ = "Henrik Høiness og Kristoffer Gjerde"
class BBCON:

    def __init__(self):
        self.behaviors = [] #En liste av alle behavior objektene som brukes av BBCON
        self.active_behaviors = [] #En liste med de aktive behavior objektene
        self.sensobs = [] #En liste av alle sensorobjektene som brukes av BBCON
        self.motobs = Motob() #En liste ac alle motor objektene som brukes av BBCON
        self.arbitrator = Arbitrator(self,True) #Arbitratoren som skal løse requests fra behaviors

        #Andre variabler kan være current_timestep, inaktive behaviors og roboten selv


    def add_behavior(self,behavior):
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def add_sensob(self,sensor):
        if sensor not in self.sensobs:
            self.sensobs.append(sensor)

    def activate_behavior(self,behavior):
        if behavior not in self.active_behaviors:
            behavior.active_flag = True
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self,behavior):
        if behavior in self.active_behaviors:
            behavior.active_flag = False
            self.active_behaviors.remove(behavior)


    # Oppdatere sensobs
    def update_sensobs(self):
        for sensob in self.sensobs:
            sensob.update()

    def reset_sensobs(self):
        for sensob in self.sensobs:
            sensob.reset()


    # Oppdatere behaviours
    def update_behaviors(self):
        for behavior in self.behaviors:
            behavior.update()

    def update_motobs(self,action):
        self.motobs.update(action)


    def run_one_timestep(self):
        #Update sensobs
        self.update_sensobs()

        #Update behaviors
        self.update_behaviors()

        print(self.active_behaviors)

        #Call arbitrator.choose_action
        action = self.arbitrator.choose_action()
        print(action)

        #Update motobs
        self.update_motobs(action)

        #Pause
        time.sleep(0.5)

        #Reset sensobs
        self.reset_sensobs()




