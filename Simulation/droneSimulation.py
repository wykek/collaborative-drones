import birdsEyeMap as bem
import cameraDrones as cd
import numpy as np
# 
class Simulation:
  def __init__(self, inMap = np.array([],np.int16)):
    self.__detailedMap = bem.DroneMap(inMap)
    self.__flyingCameras = []
    self.__cars = []

  def addAggregateMap(self, inMap):
    self.__detailedMap.copyMap(inMap)

  # Adds a camera to the simulation: requires a map and position
  # to be added before it can be used.
  # Not working
  def addFlyingCamera(self):
    np.append(self.__flyingCameras, cd.DroneFlying())
    print(self.__flyingCameras[0].getCameraMap())

  # Adds a car to the simulation: functional as long as
  # the car is present in the detailed map, but a position
  # and camera can optionally be added instead.
  # Not working
  def addCarCamera(self):
    np.append(self._cars, cd.DroneCar())
    #TODO add car check

  def addBlankMap(self, xSize, ySize):
    self.__detailedMap.copyMap(np.zeros((xSize, ySize), dtype = np.int16))

  # Not working maybe
  def addFlyingMap(self, inMap, flyingNumber):
    self.__flyingCameras[flyingNumber].addMap(inMap)
    
  # Cars are adjusted by one because python starts lists at
  # 0 but cars start at 1
  # Not working maybe
  def addCarMap(self, inMap, carNumber):
    self.__cars[carNumber - 1].addMap(inMap)

  #Not working maybe
  def addFlyingPosition(self, flyingNumber, inX, inY, inRotation):
    self.__flyingCameras[flyingNumber].setPosition(inX, inY, inRotation)

  # Cars are adjusted by one because python starts lists at
  # 0 but cars start at 1
  # Not working maybe
  def addCarPosition(self, carNumber, inX, inY, inRotation):
    self.__Cars[carNumber - 1].setPosition(inX, inY, inRotation)

  # Movement
  def moveFlyingForward(self, flyingNumber):
    self.__flyingCameras[flyingNumber].moveForward()
  def moveCarForward(self, carNumber):
    self.__cars[carNumber - 1].moveForward()
  def moveFlyingBack(self, flyingNumber):
    self.__flyingCameras[flyingNumber].moveBack()
  def moveCarBack(self, carNumber):
    self.__cars[carNumber - 1].moveBack()

  # Rotation
  def rotateFlying(self, flyingNumber):
    self.__flyingCameras[flyingNumber].rotateClockwise()
  def rotateCar(self, carNumber):
    self.__cars[carNumber - 1].rotateClockwise()
  def rotateFlyingTo(self, flyingNumber, desiredOrientation):
    self.__flyingCameras[flyingNumber].rotateToOrientation()
  def rotateCarTo(self, carNumber, desiredOrientation):
    self.__cars[carNumber - 1].rotateToOrientation()

  # Todo: Get X and Y values by adjusting for differences in camera.
  # Iterate through car and flying cameras to incorporate all changes
  def updateMap(self):
    # Update and aggregate flying drone camera information
    for cameraNumber in self.__flyingCameras:
      # Grab range of coordinates to update
      lowLeftX = self.__flyingCameras[cameraNumber].getXOffset() + \
      self.__flyingCameras[cameraNumber].getXPos()
      lowLeftY = self.__flyingCameras[cameraNumber].getYOffset() + \
      self.__flyingCameras[cameraNumber].getYPos()
      topRightX = lowLeftX + self.__flyingCameras[cameraNumber].getXViewSize()
      topRightY = lowLeftY + self.__flyingCameras[cameraNumber].getYViewSize()

      # Update map
      self.__detailedMap.revealMap(lowLeftX, lowLeftY, topRightX, topRightY, \
      self.__flyingCameras[cameraNumber].getCameraMap())

    # Update and aggregate car drone information if applicable
    for cameraNumber in self.__cars:
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
    #print(tempArray)
    for arrayrow in tempArray[::-1]:
      print(arrayrow)
