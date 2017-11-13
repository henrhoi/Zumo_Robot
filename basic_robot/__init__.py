import SensorWrappers.zumo_button as button
from sensob import IR_Sensob,Camera_Sensob,Ultrasonic_Sensob,Reflectance_Sensob
from behavior import Follow_Line,Turn
from BBCON import BBCON
from motors import Motors
__authors__ = "Henrik Høiness og Kristoffer Gjerde"

def main():

    button.ZumoButton().wait_for_press()

    bbcon = BBCON() #Lager aribator og motob selv

    #Sensob
    IR_sensob = IR_Sensob()
    Camera = Camera_Sensob()
    Ultra = Ultrasonic_Sensob()
    Reflect = Reflectance_Sensob() #Sensor under robot

    #bbcon.add_sensob(IR_Sensob)
    bbcon.add_sensob(Ultra)
    #bbcon.add_sensob(Camera)
    bbcon.add_sensob(Reflect)

    #Evt Motors
    #Motor = Motors()

    #Behaviors
    follow_line = Follow_Line(bbcon,Reflect)
    # turn_around = Turn(bbcon,IR_sensob)

    bbcon.add_behavior(follow_line)
    # bbcon.add_behavior(turn_around)

    print(bbcon.behaviors)

    while True:
       print("one timestep")
       bbcon.run_one_timesteps()

main()


