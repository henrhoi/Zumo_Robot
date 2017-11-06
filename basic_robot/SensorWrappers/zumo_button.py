__author__ = 'keithd'
import wiringpi2 as wp

class ZumoButton():

    def __init__(self):
        wp.wiringPiSetupGpio()
        wp.pinMode(22, 0)
        wp.pullUpDnControl(22, 2)

    def wait_for_press(self):
        read_val = wp.digitalRead(22)
        while read_val:
            read_val = wp.digitalRead(22)
        print("Button pressed!!")

