import numpy as np
 
class DroneMap:
  def __init__(self, inMap = np.array([],np.int16)):
    # Note: first [] is X value, second [] is Y value
    self.__map = np.array([],np.int16)
    # Unused, possibly later used for "zooming" in or out of map
    # Would determine scale
    self.__size = 1

    try:
      # Copy 2D array if it is passed to constructor
      if(inMap.size != 0):
        self.__map = (np.copy(inMap.astype('int16')))
    except:
      print("Error: invalid DroneMap initialization")

  # Fills in portion of map without replacing the whole
  def revealMap(self, lowLeftX, lowLeftY, topRightX, topRightY, inMap):
    for outIndex in range (lowLeftX, topRightX):
      for inIndex in range (lowLeftY, topRightY):
        self.__map[inIndex][outIndex] = inMap[inIndex][outIndex]

  # Replaces existing map with new map
  def copyMap(self, inMap):
    self.__map = np.copy(inMap.astype('int16'))

  def getMap(self):
    return self.__map

  def getXSize(self):
    return len(self.self.__map)

  def getYSize(self):
    if(self.__map.size != 0):
      # Maps should be rectangular, and Python 2D arrays are
      # just lists of lists, so grabbing the length of the first
      # element should give us our Y length
      return len(self.__map[0])
    else:
      print("Error: map not initialized.")

class SimplifiedMap(DroneMap):
  def __init__(self, inMap = None):
    super().__init__(inMap)
    self.__simplifyMap()

  def revealMap(self, topLeftX, topLeftY, bottomRightX, bottomRightY, inMap):
    super.revealMap(topLeftX, topLeftY, bottomRightX, bottomRightY, inMap)
    self.__simplifyMap()

  def copyMap(self, inMap):
    super.copyMap(inMap)
    self.__simplifyMap()

  def __validSimpleValue(self, cellValue):
    if cellValue == 10 or cellValue == 11 or cellValue == 0:
      return True
    else:
      return False

  def __simplifyMap(self):
    self.__validSimpleValue(4)
    for outIndex in super.__map:
      for inIndex in super.__map[outIndex]:
        if not (self.__validSimpleValue(super.__map[outIndex][inIndex])):
          # Assume other cars are passable
          if (super.__map[outIndex][inIndex] > 0 and super.__map[outIndex][inIndex] < 6):
            super.__map[outIndex][inIndex] = 10
          # Assume open doors and buttons are passable
          elif (super.__map[outIndex][inIndex] % 100 == 13):
            super.__map[outIndex][inIndex] = 10
          elif (super.__map[outIndex][inIndex] % 100 == 14):
            super.__map[outIndex][inIndex] = 10
          elif (super.__map[outIndex][inIndex] % 100 == 16):
            super.__map[outIndex][inIndex] = 10
          elif(super.__map[outIndex][inIndex] % 100 == 17):
            super.__map[outIndex][inIndex] = 10
          else:
            super.__map[outIndex][inIndex] = 11