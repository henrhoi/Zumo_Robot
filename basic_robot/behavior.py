from abc import abstractmethod

_author_ = "Kristoffer Gjerde"


"""
TODO: fix each behavior to set motor_recomendation to appropiate format [direction,speed,duration]
+ add behavior for taking picture
+ stop then take picture then deside if picture is red or not? if red Run?
"""


class Behavior:

    def __init__(self, bbcon,sensobs):
        self.bbcon = bbcon #En peker til controlleren som bruker denne behavioren
        self.sensobs = sensobs
        self.motor_recommendations = []
        self.active_flag = None #Boolean value som sier om behavior er aktiv
        self.halt_request = None
        self.priority = 0 # Viktigheten av denne behavior
        self.match_degree = 0 #Et tall mellom 0 og 1
        self.weight = 0 #priority * matchdegree

    @abstractmethod
    def consider_deactivation(self):
        #Hvis den er aktiv bør den teste om den bør deaktiveres
        return

    @abstractmethod
    def consider_activation(self):
        #Hvis deaktivert, test om den burde slås på igjen.
        return

    @abstractmethod
    def update(self):
        #Hovedoppgaver: Update acitivity flag. Kall sense_and_act. Update weight.
        return

    @abstractmethod
    def sense_and_act(self):
        #Bruker sensob readings for å lage motor recommendations (og halt_requet?..)
        return


class Follow_Line(Behavior):

    #Oppførsel for å følge en svart line under roboten
    #Bruker Reflectance_Sensors under roboten

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)
        self.threshold = 0.5 #Hvis sensoren er under denne verdien vil den returnere true når den consider_activation

    def consider_deactivation(self):
        return not self.consider_activation()

    def consider_activation(self):
        reflectance_sensor = self.sensobs #Hvis vi bare sender inn RS som sensob
        for sensor_verdi in reflectance_sensor: #Antar at de er oppdatert før denne kalles.
            if sensor_verdi < self.threshold:
                self.bbcon.active_behavior(self)
                return True

        #Hvis ikke
        self.weight = 0
        self.bbcon.deactivate_behavior(self)
        return False

    def update(self):
        self.consider_activation() # Activity flag settes i BBCON
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        #Hvis sensorene til venstre gir "mørkt" sving venstre
        #Hvis sensorene til høyre gir "mørkt" sving høyre
        sensor_array = self.sensobs
        if sensor_array[0] < self.threshold and sensor_array[5] < self.threshold:
            #Kjør framover
            self.motor_recommendations = ["f"] #Move forward
        elif sensor_array[0] < self.threshold:
            #Sving venstre
            self.motor_recommendations = ["l"] #Move left
            self.match_degree = 0.9
        elif sensor_array[5] < self.threshold:
            #Sving høyre
            self.motor_recommendations = ["r"] #Move right
        else:
            self.motor_recommendations = ["f"]
            self.match_degree = 0.5

        self.priority = 0.5



class Avoid_Collison(Behavior):
    #Stopper opp hvis hinder er nærmere enn threshold
    #Bruker ultrasonic sensor

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)
        self.threshold = 10 #cm fra hinder

    def consider_activation(self):
        less_than_threshold = self.sensobs.value < self.threshold

        if less_than_threshold:
            self.bbcon.active_behavior(self)
        else:
            self.bbcon.deactivate_behavior(self)

        return less_than_threshold

    def consider_deactivation(self):
        return not self.consider_activation()

    def update(self):
        self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        #Kjører kun hvis activeflag er True
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["s"] #Hvis metoden kjører betyr det vi må stoppe
        #Kan stoppe å ta et bilde feks?
        self.priority = 0.9
        self.match_degree = 0.9


class TakePicture(Behavior):

    #Legg in slik at den tar bilde når den stopper?
    #Bruk Camera

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)

    def consider_activation(self):
        #Skal arbitrator gi beskjed når den har stoppet?
        pass

    def consider_deactivation(self):
        return not self.consider_activation()

    def update(self):
        self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()

        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        #Motoren er stoppet?

        image = self.sensobs.value

class RUN(Behavior):

    #Bruker IRProxity sensor

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)

    def consider_activation(self):
        should_activate = self.sensobs.value[0] or self.sensobs.value[1]
        if should_activate: self.bbcon.active_behavior(self)
        else: self.bbcon.deactivate_behavior(self)
        return should_activate

    def consider_deactivation(self):
        return not self.consider_activation()


    def update(self):
        self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        #Active flag er True
        self.motor_recommendations = ["f"]
        self.match_degree = 0.9
        self.priority = 0.4










