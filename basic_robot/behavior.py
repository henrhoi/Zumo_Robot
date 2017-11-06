_author_ = "William Kvaale"

class Behavior:

    def __init__(self, bbcon):
        self.bbcon = bbcon #En peker til controlleren som bruker denne behavioren
        self.sensobs = []
        self.motor_recommendations = []
        self.active_flag = False #Boolean value som sier om behavior er aktiv
        self.halt_request = 0
        self.priority = 0 # Viktigheten av denne behavior
        self.match_degree = 0 #Et tall mellom 0 og 1
        self.weight = self.priority * self.match_degree


    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def update(self):
        pass

    def sense_and_act(self):
        pass

