__author__ = 'William Kvaale'
from basic_robot.motors import Motors

# The Arbitrator will decide which motobs that will be executed
# Motobs tell the Motors what to do
# Motors execute what's it told. How glorious!


class Motob:

    def __init__(self):
        self.motor = Motors()  # Initializing Motors, which motob will make decisions for
        self.value = []  # a holder of the most recent motor recommendation sent to the motob

    def update(self, mr):
        # Receive a motor recommendation (mr), load into value, and operationalize!
        self.value = mr  # [direction, speed, duration]
        self.operationalize()

    def operationalize(self):
        # Convert a motor recommendation into on or more motor settings,
        # which is sent back to the corresponding motors
        motor = self.motor
        for val in self.value:
            if val[0] == 'F':
                motor.forward(val[1], val[2])
            elif val[0] == 'B':
                motor.backward(val[1], val[2])
            elif val[0] == 'R':
                motor.right(val[1], val[2])
            elif val[0] == 'L':
                motor.left(val[1], val[2])
            elif val[0] == "S":
                motor.stop()

