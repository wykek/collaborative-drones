import birdsEyeMap as bem
import numpy as np

class DroneCamera:
    def __init__(self, inX=None, inY=None, inRotation=0):
        # Stores where the map starts in relation to the drone's position
        self.__offsetX = 0
        self.__offsetY = 0

        self.__movement = None

        self.__thisDroneMap = bem.DroneMap()
        # Position is set at initialization
        if (str(inX).isnumeric() and inY != None and inRotation != None):
            self.__droneX = np.int32(inX)
            self.__droneY = np.int32(inY)
            self.__droneRotation = np.int8(inRotation)
            self.__validPosition = True
            self.__validCamera = False
        # Position is unset, need to input it later with setPosition
        # before object is used for most things
        else:
            self.__droneX = None
            self.__droneY = None
            self.__droneRotation = None
            self.__validPosition = False
            self.__validCamera = False

    # Initializes the map or replaces the camera's map with a new one
    # Takes a 2D list as an input. The list must be "rectangular"
    def addMap(self, inMap):
        self.__thisDroneMap.copyMap(inMap)
        self.__validCamera = True

    # Fills in portion of map without replacing the whole
    def updateMap(self, topLeftX, topLeftY, bottomRightX, bottomRightY, inMap):
        self.__thisDrone.revealMap(topLeftX, topLeftY, bottomRightX, bottomRightY, inMap)

    def setPosition(self, inX, inY, inRotation):
        self.__droneX = np.int16(inX)
        self.__droneY = np.int16(inY)
        self.__droneRotation = np.int8(inRotation)
        self.__validPosition = True

    # Generic Accessors
    # Position
    def getXPos(self):
        return self.__droneX

    def getYPos(self):
        return self.__droneY

    def getRotation(self):
        return self.__droneRotation

    # Map
    def getCameraMap(self):
        if self.__validCamera == False:
            print("Error: map uninitialized.")
            return np.array([0], np.int16)
        else:
            return self.__thisDroneMap.getMap()

    # Map Dimensions
    def getXViewSize(self):
        return self.__thisDroneMap.getXSize()

    def getYViewSize(self):
        return self.__thisDroneMap.getYSize()

    # Offsets
    def getXOffset(self):
        return self.__offsetX

    def getYOffset(self):
        return self.__offsetY

    # Movement
    def moveForward(self):
        if (self.__validPosition == True):
            # Increase X when facing east, or decrease for west
            if (self.__droneRotation > 1 and self.__droneRotation < 5):
                self.__droneX += 1
            elif (self.__droneRotation > 5):
                self.__droneX -= 1

            # Increase X when facing north, or decrease for south
            if (self.__droneRotation > 7 or self.__droneRotation < 3):
                self._droneY += 1
            elif (self.__droneRotation > 3 and self.__droneRotation < 7):
                self.droneY -= 1
        else:
            print("Error: movement without position. \n")

    def moveBack(self):
        if (self.__validPosition == True):
            # Decrease X when facing east, or increase for west
            if (self.__droneRotation > 1 and self.__droneRotation < 5):
                self.__droneX -= 1
            elif (self.__droneRotation > 5):
                self.__droneX += 1

            # Decrease X when facing north, or increase for south
            if (self.__droneRotation > 7 or self.__droneRotation < 3):
                self._droneY -= 1
            elif (self.__droneRotation > 3 and self.__droneRotation < 7):
                self.droneY += 1
        else:
            print("Error: movement without position. \n")

    # Rotation
    def rotateClockwise(self):
        if (self.__validPosition == True):
            # Scale goes from 1-8 for rotation, so wrap around back to 1
            # 1 is north, 5 is south
            if (self.__droneRotation == 8):
                self.__droneRotation = 1
            else:
                self.__droneRotation += 1
        else:
            print("Error: attempted rotation without position. \n")

    def rotateCounterClockwise(self):
        if (self.__validPosition == True):
            # Scale goes from 1-8 for rotation, so wrap around back to 8
            if (self.__droneRotation == 1):
                self.__droneRotation = 8
            else:
                self.__droneRotation -= 1
        else:
            print("Error: attempted rotation without position. \n")

    def rotateToOrientation(self, desiredOrientation):
        while self.__droneRotation != desiredOrientation:
            self.rotateCounterClockwise()



# To add: flying specific modifications
class DroneFlying(DroneCamera):
    def __init__(self, inX=None, inY=None, inRotation=0):
        super().__init__(inX, inY, inRotation)


# To add: car specific modifications
class DroneCar(DroneCamera):
    def __init__(self, inX=None, inY=None, inRotation=0):
        super().__init__(inX, inY, inRotation)

    def attachedCameraCheck(self):
        return (self.__validPosition and self.__validCamera)