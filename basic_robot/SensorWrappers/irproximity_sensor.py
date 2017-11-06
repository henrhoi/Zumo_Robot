import RPi.GPIO as GPIO

#Hver side av roboten har en proximity sensor. Er True hvis et object er nærmere enn 5 cm (3cm). False ellers
class IRProximitySensor:
    def __init__(self):
        self.value = None
        self.read_pin_1 = 8
        self.read_pin_2 = 10
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)

    def get_value(self):
        return self.value

    def update(self):
        self.value = self.sensor_get_value()
        return self.value

    def reset(self):
        self.value = None

    def sensor_get_value(self):
        GPIO.setup(self.read_pin_1, GPIO.IN)
        GPIO.setup(self.read_pin_2, GPIO.IN)
        read_val_1 = GPIO.input(self.read_pin_1)
        read_val_2 = GPIO.input(self.read_pin_2)
        # Invert the values, so that True means something is close
        return [not read_val_1, not read_val_2]
