import birdsEyeMap as bem
import cameraDrones as cd
import numpy as np
import socket

#
class Controller:
    def __init__(self, inMap=np.array([], np.int16)):
        self.__detailedMap = bem.DroneMap(inMap)
        self.__flyingCameras = []
        self.__cars = []

        self.__commandLength = 5
        self.__carSockets = []
        self.__acceptedSockets = []

    def getMap(self):
        self.__detailedMap.getMap()

    def addAggregateMap(self, inMap):
        self.__detailedMap.copyMap(inMap)

    # Adds a camera to the simulation: requires a map and position
    # to be added before it can be used.
    # Not working
    def addFlyingCamera(self):
        self.__flyingCameras.append(cd.DroneFlying())

    # Adds a car to the simulation: functional as long as
    # the car is present in the detailed map, but a position
    # and camera can optionally be added instead.
    # Not working
    def addCarCamera(self):
        self.__cars.append(cd.DroneCar())
        thisCar = len(self.__cars) - 1
        portNumber = 1093
        try:
            configName = "config" + str(thisCar + 1) + ".txt"
            conFile = open(configName, 'r')
            # First line of config file is port
            portNumber = conFile.read()
            portNumber = int(conFile.read())
            conFile.close()
        except:
            portNumber = 1093  # No config file found, use default ports

        # Set up a socket to actually control the car
        self.__carSockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.__carSockets[thisCar].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.__carSockets[thisCar].bind(('10.20.27.193', portNumber))
        self.__carSockets[thisCar].bind(('127.0.0.1', 1234))
        self.__acceptedSockets.append(" ") # Placeholder replaced in loop
        self.__carSockets[thisCar].listen(5)
        while True:
            self.__acceptedSockets[thisCar], address = self.__carSockets[thisCar].accept()
            print("Here too")

        # TODO add car check

    def addBlankMap(self, xSize, ySize):
        self.__detailedMap.copyMap(np.zeros((xSize, ySize), dtype=np.int16))

    def addFlyingMap(self, inMap, flyingNumber):
        self.__flyingCameras[flyingNumber].addMap(inMap)

    # Cars are adjusted by one because python starts lists at
    # 0 but cars start at 1
    def addCarMap(self, inMap, carNumber):
        self.__cars[carNumber - 1].addMap(inMap)

    # Not working maybe
    def addFlyingPosition(self, flyingNumber, inX, inY, inRotation):
        self.__flyingCameras[flyingNumber].setPosition(inX, inY, inRotation)

    # Cars are adjusted by one because python starts lists at
    # 0 but cars start at 1
    def addCarPosition(self, carNumber, inX, inY, inRotation):
        self.__cars[carNumber - 1].setPosition(inX, inY, inRotation)

    # Movement
    def moveFlyingForward(self, flyingNumber):
        self.__flyingCameras[flyingNumber].moveForward()

    def moveCarForward(self, carNumber):
        self.__cars[carNumber - 1].moveForward()
        print("Bye ")

        # Send the signal to the car to go
        while True:
            # Mutual connection established
            try:
                targetSocket, address = self.__carSockets[carNumber - 1].accept()
                print("I hate sockets")


                # 1 will mean go forward
                outCommand = "1"
                outCommand = f"{len(outCommand):<{self.__commandLength}}" + outCommand

                print(str(self.__commandLength))
                targetSocket.send(bytes(outCommand, "utf-8"))
                print(str(outCommand))
            except:
                pass

    def moveFlyingBack(self, flyingNumber):
        self.__flyingCameras[flyingNumber].moveBack()

    def moveCarBack(self, carNumber):
        self.__cars[carNumber - 1].moveBack()

        # Send the signal to the car to go
        while True:
            # Mutual connection established
            targetSocket, address = self.__carSockets[carNumber - 1].accept()

            # 2 will mean go back
            outCommand = "2"
            outCommand = f"{len(outCommand):<{self.__commandLength}}" + outCommand

            targetSocket.send(bytes(outCommand, "utf-8"))

    # Rotation
    def rotateFlying(self, flyingNumber):
        self.__flyingCameras[flyingNumber].rotateClockwise()

    def rotateCar(self, carNumber):
        self.__cars[carNumber - 1].rotateClockwise()

        # Send the signal to the car to go
        while True:
            # Mutual connection established
            targetSocket, address = self.__carSockets[carNumber - 1].accept()

            # 3 will mean turn clockwise
            outCommand = "3"
            outCommand = f"{len(outCommand):<{self.__commandLength}}" + outCommand

            targetSocket.send(bytes(outCommand, "utf-8"))

    def rotateFlyingTo(self, flyingNumber, desiredOrientation):
        self.__flyingCameras[flyingNumber].rotateToOrientation()

    def rotateCarTo(self, carNumber, desiredOrientation):
        self.__cars[carNumber - 1].rotateToOrientation()

        # Send the signal to the car to go
        while True:
            # Mutual connection established
            targetSocket, address = self.__carSockets[carNumber - 1].accept()

            # 1 will mean go counter clockwise
            outCommand = "4"
            outCommand = f"{len(outCommand):<{self.__commandLength}}" + outCommand

            targetSocket.send(bytes(outCommand, "utf-8"))

    # Todo: Get X and Y values by adjusting for differences in camera.
    # Iterate through car and flying cameras to incorporate all changes
    def updateMap(self):
        # Update and aggregate flying drone camera information
        for cameraNumber in range(0, len(self.__flyingCameras)):
            # Grab range of coordinates to update
            lowLeftX = self.__flyingCameras[cameraNumber].getXOffset() \
                       + self.__flyingCameras[cameraNumber].getXPos()
            lowLeftY = self.__flyingCameras[cameraNumber].getYOffset() \
                       + self.__flyingCameras[cameraNumber].getYPos()
            topRightX = lowLeftX + self.__flyingCameras[cameraNumber].getXViewSize()
            topRightY = lowLeftY + self.__flyingCameras[cameraNumber].getYViewSize()

            # Update map
            self.__detailedMap.revealMap(lowLeftX, lowLeftY, topRightX, topRightY, \
                                         self.__flyingCameras[cameraNumber].getCameraMap())

        # Update and aggregate car drone information if applicable
        for cameraNumber in range(0, len(self.__cars)):
            if self.__cars[cameraNumber].attachedCameraCheck() == True:
                # Grab range of coordinates to update
                lowLeftX = self.__cars[cameraNumber].getXOffset() + \
                           self.__cars[cameraNumber].getXPos()
                lowLeftY = self.__cars[cameraNumber].getYOffset() + \
                           self.__cars[cameraNumber].getYPos()
                topRightX = lowLeftX + self.__cars[cameraNumber].getXViewSize()
                topRightY = lowLeftY + self.__cars[cameraNumber].getYViewSize()

                # Update map
                self.__detailedMap.revealMap(lowLeftX, lowLeftY, topRightX, topRightY, \
                                             self.__cars[cameraNumber].getCameraMap())

    def printSimulation(self):
        tempArray = self.__detailedMap.getMap()
        # print(tempArray)
        for arrayrow in tempArray[::-1]:
            print(arrayrow)
