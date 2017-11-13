from abc import abstractmethod

_author_ = "Kristoffer Gjerde"


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
        #Hvis den er aktiv bor den teste om den bor deaktiveres
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

    def __repr__(self):
        return str(type(self))

    def __str__(self):
        return str(type(self))

class Follow_Line(Behavior):

    #Oppforsel for å folge en svart line under roboten
    #Bruker Reflectance_Sensors under roboten

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)
        self.threshold = 0.1 #Hvis sensoren er under denne verdien vil den returnere true når den consider_activation


    def consider_activation(self):
        self.bbcon.activate_behavior(self)
        return True


    def update(self):
        self.consider_activation() # Activity flag settes i BBCON
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        #Hvis sensorene til venstre gir "morkt" sving venstre
        #Hvis sensorene til hoyre gir "morkt" sving hoyre
        sensor_array = self.sensobs.value
        if sensor_array[0] > self.threshold and sensor_array[5] > self.threshold:
            self.motor_recommendations = ["B",0.5,0.75]
        elif sensor_array[0] > self.threshold:

            self.motor_recommendations = ["R",0.5,1]
            self.match_degree = 0.9
        elif sensor_array[5] > self.threshold:

            self.motor_recommendations = ["L",0.5,1]
        else:
            self.motor_recommendations = ["F",0.5,0.1]
            self.match_degree = 0.6

        self.priority = 1


class Turn(Behavior):
    #Stopper opp hvis hinder er nærmere enn threshold
    #Bruker ultrasonic sensor

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)

    def consider_activation(self):
        self.bbcon.activate_behavior(self)
        return True

    def consider_deactivation(self):
        return not self.consider_activation()

    def update(self):
        self.consider_activation()


        if not self.active_flag:
            self.weight = 0
            return

        #Kjorer kun hvis activeflag er True
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["T"] #Turn arround
        self.priority = 0.9
        self.match_degree = 0.9


class AvoidCollison(Behavior):

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)
        self.threshold = 10 #cm

    def consider_activation(self):
        if self.sensobs.value < self.threshold:
            self.bbcon.activate_behavior(self)
            print("NEI")
            return True

    def update(self):
        self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        md = 1 / (self.sensobs.value / 10)
        if md > 1: md = 0.99
        self.bbcon.take_pic = self.sensobs.value <= 10

        self.motor_recommendations = ["S"]  #Stop
        self.priority = 1.0
        self.match_degree = md

class TakePicture(Behavior):

    #Legg in slik at den tar bilde når den stopper?
    #Bruk Camera

    def __init__(self,bbcon,sensobs):
        Behavior.__init__(self,bbcon,sensobs)

    def consider_activation(self):
        if self.bbcon.take_pic:
            self.bbcon.activate_behavior(self)
        else:
            print("deaktiver bilde")
            self.bbcon.deactivate_behavior(self)


    def update(self):
        self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()

        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        image = self.sensobs.value #ImageObj
        r,g,b = image.getpixel((32,32))
        if g == max(r,g,b):
            self.motor_recommendations = ["G"]
            self.priority = 1
            self.match_degree = 1
        else: self.priority=0












