import PCA9685
import time
from Motor import Motor

# A parent class which all robot classes with movement can inherit from
class Movement:
    def __init__(self):
        self.waitScale = 1
        self.powerScale = 1
        self.forOff = 1
        self.backOff = 1
        self.COff = 1
        self.CCOff = 1
    def moveForward(self):
        forOff = 1
        self.setMotorModel(2000 * self.waitScale * self.forOff, 2000 * \
        self.waitScale * self.forOff, 2000 * self.waitScale * self.forOff, \
        2000 * self.waitScale * self.forOff)
        time.sleep(3 * self.waitScale)
        self.setMotorModel(0, 0, 0, 0) # Stop after moving
    def moveBackward(self):
        forOff = 1
        self.setMotorModel(-2000 * self.waitScale * self.backOff, -2000 * \
        self.waitScale * self.backOff, -2000 * self.waitScale * self.backOff, \
        -2000 * self.waitScale * self.backOff)
        time.sleep(3 * self.waitScale)
        self.setMotorModel(0, 0, 0, 0) # Stop after moving
    def turnClockwise(self):
        forOff = 1
        self.setMotorModel(-500 * self.waitScale * self.COff, -500 * \
        self.waitScale * self.COff, 2000 * self.waitScale * self.COff, \
        2000 * self.waitScale * self.COff)
        time.sleep(3 * self.waitScale)
        self.setMotorModel(0, 0, 0, 0) # Stop after moving
    def turnCClockwise(self):
        forOff = 1
        self.setMotorModel(2000 * self.waitScale * self.CCOff, 2000 * \
        self.waitScale * self.CCOff, -500 * self.waitScale * self.CCOff, \
        -500 * self.waitScale * self.CCOff)
        time.sleep(3 * self.waitScale)
        self.setMotorModel(0, 0, 0, 0) # Stop after moving
    def setMotorModel(self, duty1, duty2, duty3, duty4):
        pass

# A class for moving the car. Inherits from the movement
# parent class as well as the motor class
class CarMovement(Motor, Movement):
    def __init__(self):
        super().__init__(self)

        # Tweak after testing
        # Modify power and time delivery to proper
        # scale for drone model
        self.waitScale = 1
        self.powerScale = 1
        self.forOff = 1
        self.backOff = 1
        self.COff = 1
        self.CCOff = 1
