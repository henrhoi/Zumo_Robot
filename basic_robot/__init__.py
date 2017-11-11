import SensorWrappers.zumo_button as button
from sensob import IR_Sensob,Camera_Sensob,Ultrasonic_Sensob,Reflectance_Sensob
from behavior import Follow_Line,Avoid_Collison
from BBCON import BBCON
from motors import Motors
__authors__ = "Henrik Høiness og Kristoffer Gjerde"

def main():

    m = Motors()
    m.forward(.5,1)
    m.backward(.5,1)
    m.right(.7,2)
    m.left(.7,2)
    m.backward(.5,0.5)
    m.set_value([.6,.3],2)
    m.set_value([-.6,-.3],2)
    button.ZumoButton().wait_for_press()

    bbcon = BBCON() #Lager aribator og motob selv

    #Sensob
    IR_sensob = IR_Sensob()
    Camera = Camera_Sensob()
    Ultra = Ultrasonic_Sensob()
    Reflect = Reflectance_Sensob() #Sensor under robot

    #bbcon.add_sensob(IR_Sensob)
    bbcon.add_sensob(Ultra)
    bbcon.add_sensob(Camera)
    bbcon.add_sensob(Reflect)

    #Evt Motors
    #Motor = Motors()

    #Behaviors
    follow_line = Follow_Line(bbcon,Reflect)
    avoid_collison = Avoid_Collison(bbcon,Ultra)

    bbcon.add_behavior(follow_line)
    bbcon.add_behavior(avoid_collison)

    #while True:
    #    print("kug")
    #    bbcon.run_one_timesteps()

main()


