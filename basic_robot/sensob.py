from abc import abstractmethod

oversjef = "Henrik"

from basic_robot.SensorWrappers import camera,irproximity_sensor,reflectance_sensors


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
        self.value = self.camera.update()
        return self.value


class IR_Sensob(Sensob):

    def __init__(self):
        Sensob.__init__(self)
        self.IR = irproximity_sensor.IRProximitySensor()
        self.value = None

    def update(self):
        self.value = self.IR.update()
        return self.value


class Reflectance_Sensob(Sensob):

    def __init__(self):
        Sensob.__init__(self)
        self.reflectance = reflectance_sensors.ReflectanceSensors()
        self.value = None

    def update(self):
        self.value = self.reflectance.update()
        return self.value



