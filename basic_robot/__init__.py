from time import sleep
import random
import imager2 as IMR
from motors import Motors
import SensorWrappers.zumo_button as button
from sensob import IR_Sensob,Camera_Sensob,Ultrasonic_Sensob,Reflectance_Sensob
from behavior import Follow_Line,Avoid_Collison
from BBCON import BBCON
__authors__ = "Henrik Høiness og Kristoffer Gjerde"

if __name__ == '__main__':
    button.ZumoButton().wait_for_press()

    bbcon = BBCON() #Lager aribator og motob selv

    #Sensob
    IR_sensob = IR_Sensob()
    Camera = Camera_Sensob()
    Ultra = Ultrasonic_Sensob()
    Reflect = Reflectance_Sensob() #Sensor under robot

    bbcon.add_sensob(IR_Sensob)
    bbcon.add_sensob(Ultra)
    bbcon.add_sensob(Camera)
    bbcon.add_sensob(Reflect)

    #Evt Motors
    #Motor = Motors()

    #Behaviors
    follow_line = Follow_Line(bbcon,Reflect)
    avoid_collison = Avoid_Collison(bbcon,Ultra)

    bbcon.add_sensob(follow_line)
    bbcon.add_sensob(avoid_collison)

    while True:
        bbcon.run_one_timestep()


