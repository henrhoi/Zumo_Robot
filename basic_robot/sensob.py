from abc import abstractmethod

__author__ = "Henrik Høiness"

from SensorWrappers import camera, irproximity_sensor, reflectance_sensors, ultrasonic


class Sensob:

    def __init__(self):
        self.value = None

    @abstractmethod
    def update(self):
        #Fetch relevant sensor values from the sensor wrapper
        #Convert ionto sensob value
        return

    def reset(self):
        self.value = None



class Camera_Sensob(Sensob):

    def __init__(self):
        Sensob.__init__(self)
        self.camera = camera.Camera()

    def update(self):
        # Value blir imagefil
        self.camera.update()
        self.value = self.camera.get_value()
        print("Camera: ")
        return self.value


class IR_Sensob(Sensob):

    def __init__(self):
        Sensob.__init__(self)
        self.IR = irproximity_sensor.IRProximitySensor()
        self.value = False

    def update(self):
        # Value = True/False

        self.IR.update()
        self.value = self.IR.get_value()
        print("IR_sensor: " + str(self.value))
        return self.value

class Ultrasonic_Sensob(Sensob):

    def __init__(self):
        Sensob.__init__(self)
        self.ultrasonic = ultrasonic.Ultrasonic()
        self.value = None

    def update(self):
        self.ultrasonic.update()
        self.value = self.ultrasonic.get_value()
        print("Ultrasonic: " + str(self.value))
        return self.value

class Reflectance_Sensob(Sensob):

    def __init__(self):
        Sensob.__init__(self)
        self.reflectance = reflectance_sensors.ReflectanceSensors()
        self.value = None

    def update(self):
        # Value blir [X,X,X,X,X,X] der X-->0 betyr mørkt og X-->1 betyr lyst

        self.reflectance.update()
        self.value = self.reflectance.get_value()
        print("Reflect: " + str(self.value))
        return self.value



