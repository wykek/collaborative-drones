import numpy as np
import json
import random

# connection types:
# upConnections - A slight misnomer, openings on north of map
# rightConnections - A slight misnomer, openings on east of map
# downConnections - A slight misnomer, openings on south of map
# leftConnections - A slight misnomer, openings on west of map

# Connection key:
# c - closed connection
# w - wide width
# n - narrow width
# o - ordinary width
# m - middle
# l - left from perspective of looking outside straight at that wall
# r - left from perspective of looking outside straight at that wall

# difficulty key:
# 0 - Fairly straightforward, the room mainly just requires going
#     from one side to the other.

# challenges key:
# "unknown" - Room has at least one tile that is not known.
# "open room" - Room is largely empty in the center.
# "closed corners" - Room has walls around the corner.

class MapGenerator:
    def __init__(self, inX=None, inY=None):
        self.mapSettings = {}
        self.chunkList = []
        self.__logName = None

        # Load the randomizer config
        with open("random chunks.json") as config_file:
            self.mapSettings = json.load(config_file)

        # Determines how big the map to generate is
        # Default is 100 x 100
        if inX == None and inY == None:
            self.__boundsX = 100
            self.__boundsY = 100
        else:
            self.__boundsX = inX
            self.__boundsY = inY

    def validOpeningCheck (self, thisConList, outConList):
        inMiddle = False
        inSideMiddle = False
        inSideLeft = False
        inSideRight = False
        inClosed = False
        outMiddle = False
        outSideMiddle = False
        outSideLeft = False
        outSideRight = False
        outClosed = False

        validFound = False

        for index in range(0, len(thisConList)):
            if(thisConList[index] == "w"):
                if (outConList[0] != "c"):
                    return True
            elif (thisConList[index] == "o"):
                inSideMiddle = True
            elif (thisConList == "m"):
                inMiddle = True
            elif (thisConList[index] == "l"):
                inSideLeft = True
            elif(thisConList[index] == "r"):
                inSideRight = True
            elif(thisConList[index] == "c"):
                inClosed = True

        for index in range(0, len(outConList)):
            if(outConList[index] == "w"):
                if (thisConList[0] != "c"):
                    return True
            elif (thisConList[index] == "o"):
                inSideMiddle = True
            elif (thisConList == "m"):
                inMiddle = True
            elif (thisConList[index] == "l"):
                inSideLeft = True
            elif(thisConList[index] == "r"):
                inSideRight = True
            elif(thisConList[index] == "c"):
                inClosed = True

        # Return if only one is closed
        if((inClosed and not outClosed) or (outClosed and not inClosed)):
            return False
        elif(inMiddle and outMiddle):
            return True
        elif ((inSideLeft and outSideRight) or (inSideRight and outSideRight)):
            return True
        elif ((inMiddle and inSideMiddle and outSideMiddle) or (outMiddle and outSideMiddle and inSideMiddle)):
            return True
        else:
            return False
    def createMap(self, inX=None, inY=None):
        # Make sure it is evenly divisible by chunk sizes
        inX = inX - (inX % 10)
        inY = inY - (inY % 10)

        # Determines how big the map to generate is
        # Default is 100 x 100
        if inX != None and inY != None:
            self.__boundsX = inX
            self.__boundsY = inY

        # Create miniature map to store chunks
        # and initialize it to the unknown map chunk
        self.chunkList = []
        for index in range (0, self.__boundsX / 10):
            self.chunkList.insert([])
            for inIndex in range (0, self.__boundsY / 10):
                self.chunkList[index].insert(0)

        # Iterate through, randomly picking chunks with
        # compatible opposite connections, ie. a west
        # chunk with an open east connection and
        # a right with an open west connection,
        # or closed both if they are closed.
        for index in range (0, self.__boundsX / 10):
            for inIndex in range (0, self.__boundsY / 10):
                # Grab a random chunk and see if it is compatible
                # those around it, and retry until it gets one.
                foundValid = False
                testIndex = 0
                while (foundValid == False):
                    # Assume it's true now unless disproven later
                    foundValid = True
                    testIndex = random.randrange(len(self.mapSettings["chunks"]))

                    # Test compatibility of each side
                    # North side
                    if(inIndex > 0 and (self.validOpeningCheck(self.mapSettings["chunks"][inIndex]["upConnections"],\
                       self.mapSettings["chunks"][self.chunkList[index][inIndex - 1]]["downConnections"])) == False):
                        foundValid = False
                    # South side
                    elif(inIndex <= len(self.chunkList) and not (self.validOpeningCheck( \
                         self.mapSettings["chunks"][inIndex]["downConnections"], \
                         self.mapSettings["chunks"][self.chunkList[index][inIndex + 1]]["upConnections"]))):
                        foundValid = False
                    # East side
                    elif(inIndex > 0 and not (self.validOpeningCheck (self.mapSettings["chunks"][inIndex]["upConnections"], \
                         self.mapSettings["chunks"][self.chunkList[index][inIndex - 1]]["downConnections"]))):
                        foundValid = False
                    # West side
                    elif(inIndex <= len(self.chunkList[0]) and not (self.validOpeningCheck ( \
                         self.mapSettings["chunks"][inIndex]["leftConnections"], \
                         self.mapSettings["chunks"][self.chunkList[index + 1][inIndex]]["rightConnections"]))):
                        foundValid = False

                # Assign this random chunk and move onto the next.
                self.chunkList[index][inIndex] = testIndex

        # Print map to debug lof if enabled
        if (self.__logName != None):
            with open(self.__logName, "a") as logFile:
                # Print debug array
                for index in range(0, len(self.chunkList)):
                    for inIndex in range(0, len(self.chunkList[0])):
                        logFile.write(self.chunkList[index][inIndex])
                    logFile.write("\n")

                # Print challenges
                for index in range(0, len(self.chunkList)):
                    for inIndex in range(0, len(self.chunkList[0])):
                        logFile.write(self.mapSettings["chunks"][self.chunkList[index][inIndex]]["challenges"])
                        logFile.write("  -  ")
                    logFile.write("\n")
    def setBounds(self, inX, inY):
        if inX is not None and inY is not None:
            self.__boundsX = 100
            self.__boundsY = 100

    def setLogging(self, inLogFileName):
        self.__logName = inLogFileName

if __name__ == '__main__':
    testarray2 = np.array([[4, 5, 7, 9], [5, 6, 2, 5], [1, 7, 2, 9], [1, 5, 9, 8]], np.int16)
    # Fully unknown location
    chunk1 = testarray2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]\
                                       , np.int16)
    # Open room with wall corners
    chunk2 = np.array([[10, 10, 10, 11, 11, 11, 11, 10, 10, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 10, 10, 11, 11, 11, 11, 10, 10, 10],]\
                                       , np.int16)

    # Open room with wall corners, smaller openings
    chunk3 = np.array([[10, 10, 10, 10, 11, 11, 10, 10, 10, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 10, 10, 10, 11, 11, 10, 10, 10, 10],]\
                                       , np.int16)

    # Open room with walls but open corners
    # Difficulty 0
    # Learn to ignore irrelevant open spaces,
    # don't only look between two corners.
    chunk4 = np.array([[11, 11, 11, 10, 10, 10, 10, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 11, 10, 10, 10, 10, 11, 11, 11],]\
                                       , np.int16)

    # Open room with walls but open corners, tighter opening
    # Difficulty 0
    # Learn to ignore irrelevant open spaces,
    # don't only look between two corners.
    chunk5 = np.array([[11, 11, 10, 10, 10, 10, 10, 10, 11, 11],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [10, 11, 11, 11, 11, 11, 11, 11, 11, 10],\
                       [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],\
                       [11, 11, 10, 10, 10, 10, 10, 10, 11, 11],]\
                                       , np.int16)

