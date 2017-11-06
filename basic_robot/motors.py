#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import wiringpi2 as wp


class Motors():
    def __init__(self):
        self.setup()

    def setup(self):
        self.max = 1024
        self.high = 500
        self.normal = 300
        self.low = 100

        wp.wiringPiSetupGpio()

        wp.pinMode(18, 2)
        wp.pinMode(19, 2)
        wp.pinMode(23, 1)
        wp.pinMode(24, 1)

        self.set_left_dir(0)  # Set rotation direction to forward for both wheels
        self.set_right_dir(0)

        self.freq = 400  # PWM frequency
        self.dc = 0  # Duty cycle
        print("Completed setting up motors!")

    # For the following motion commands, the speed is in the range [-1, 1], indicating the fraction of the maximum
    # speed, with negative values indicating that the wheel will spin in reverse. The argument "dur" (duration)
    # is the time (in seconds) that the action will persist.

    def forward(self, speed=0.25, dur=None):
        self.dc = int(self.max * speed)
        self.set_left_dir(0)
        self.set_right_dir(0)
        self.set_left_speed(self.dc)
        self.set_right_speed(self.dc)
        self.persist(dur)

    def backward(self, speed=0.25, dur=None):
        self.dc = int(self.max * speed)
        self.set_left_dir(1)
        self.set_right_dir(1)
        self.set_left_speed(self.dc)
        self.set_right_speed(self.dc)
        self.persist(dur)

    def left(self, speed=0.25, dur=None):
        s = int(self.max * speed)
        if self.dc == 0:
            self.set_left_dir(1)
            self.set_left_speed(s)
            self.set_right_dir(0)
            self.set_right_speed(s)
        else:
            self.set_left_speed(150)
            self.set_right_speed(450)
        self.persist(dur)

    def right(self, speed=0.25, dur=None):
        s = int(self.max * speed)
        if self.dc == 0:
            self.set_left_dir(0)
            self.set_left_speed(s)
            self.set_right_dir(1)
            self.set_right_speed(s)
        else:
            self.set_left_speed(450)
            self.set_right_speed(150)
        self.persist(dur)


    def stop(self):
        self.dc = 0
        self.set_left_speed(self.dc)
        self.set_right_speed(self.dc)

    # Val should be a 2-element vector with values for the left and right motor speeds, both in the range [-1, 1].
    def set_value(self, val,dur=None):
        left_val = int(self.max * val[0])
        right_val = int(self.max * val[1])

        # If we pass negative values to the motors, we need to reverse the direction of the motor
        self.set_left_dir(1) if (left_val < 0) else self.set_left_dir(0)
        self.set_right_dir(1) if (right_val < 0) else self.set_right_dir(0)

        # Set speed to the absolute value of the passed values
        self.set_left_speed(abs(left_val))
        self.set_right_speed(abs(right_val))
        self.persist(dur)

    # These are lower-level routines that translate speeds and directions into write commands to the motor output pins.

    def set_left_speed(self, dc):
        wp.pwmWrite(18, dc)

    def set_right_speed(self, dc):
        wp.pwmWrite(19, dc)

    def set_left_dir(self, is_forward):
        wp.digitalWrite(23, is_forward)  # 0 is forward so if they pass 1 we 'not' it

    def set_right_dir(self, is_forward):
        wp.digitalWrite(24, is_forward)  # 0 is forward so if they pass 1 we 'not' it


    def persist(self, duration):
        if duration:
            sleep(duration)
            self.stop()

