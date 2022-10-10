import numpy as np
import math
import birdsEyeMap as bem

# Return codes:
# 0 - Do nothing
# 1 - Move forward
# 2 - Turn counter-clockwise
# 3 - Turn Clockwise
def convertMovement(initX, initY, initLayer, finalX, finalY, finalLayer):
    xDist = finalX - initX
    yDist = finalY - initY
    layerDist = finalLayer - initLayer
    if (xDist != 0):
        # Move forward
        return 1
    elif (yDist != 0):
        # Move forward
        return 1
    elif (layerDist != 0):
        if (initLayer == 0):
            if (finalLayer != 7):
                # Turn CC
                return 2
            else:
                # Turn clockwise
                return 3
        elif (initLayer == 7):
            if(finalLayer != 0):
                # Turn CC
                return 2
            else:
                # Turn clockwise
                return 3
        elif (layerDist > 0):
            # Turn clockwise
            return 3
        else:
            # Turn CC
            return 2
    return 0

# Uses simply the 3D distance formula, and converts it into an integer
# to insure it truncates and rounds down. Any orientation is fine, so
# Z distance will be 0.
# 3D distance = sqrt of ((x2-x1) ^ 2 + (y2-y1) ^ 2 + (z2-z1) ^ 2)
def distanceHeuristic(initX, initY, finalX, finalY):
    return int(math.sqrt(((finalX - initX) * (finalX - initX))+ \
                         ((finalY - initY) * (finalY - initY))))

# Do a simple manual binary search to find angle coordinate case
def calForwardX(inX, inLayer):
    if(inX > 3):
        if(inLayer > 5):
            if (inLayer > 6):
                # 7 - Northwest
                return inX - 1
            else:
                # 6 - West
                return inX - 1
        else:
            if (inLayer > 4):
                # 5 - Southwest
                return inX - 1
            else:
                # 4 - South
                return inX
    else:
        if(inLayer > 1):
            if (inLayer > 2):
                # 3 - Southeast
                return inX + 1
            else:
                # 2 - East
                return inX + 1
        else:
            if (inLayer > 0):
                # 1 - Northeast
                return inX + 1
            else:
                # 0 - North
                return inX

# Do a simple manual binary search to find angle coordinate case
def calForwardY(inY, inLayer):
    if(inLayer > 3):
        if(inLayer > 5):
            if (inLayer > 6):
                # 7 - Northwest
                return inY + 1
            else:
                # 6 - West
                return inY
        else:
            if (inLayer > 4):
                # 5 - Southwest
                return inY - 1
            else:
                # 4 - South
                return inY - 1
    else:
        if(inLayer > 1):
            if (inLayer > 2):
                # 3 - Southeast
                return inY - 1
            else:
                # 2 - East
                return inY
        else:
            if (inLayer > 0):
                # 1 - Northeast
                return inY + 1
            else:
                # 0 - North
                return inY + 1

# As the coordinates go 0-7, turning left is just
# as simple as reducing by one, except
# when it is at 0 and needs to wrap around to 7
def calcCCAngle(inLayer):
    if (inLayer != 0):
        return inLayer - 1
    else:
        return 7

# As the coordinates go 0-7, turning right is just
# as simple as incrementing by one, except
# when it is at 7 and needs to wrap around to 0
def calcCAngle(inLayer):
    if (inLayer != 7):
        return inLayer + 1
    else:
        return 0

"""
class aStarQueue():
    def __init__(self, inH=None):
        # Set up fonts
        self.mapFont = pygame.font.SysFont('Corbel', 25)
        self.maxSize = 100
        """

# Gets a list with three items for the X, Y, and Rotation.
# Checks if any items in a list of lists contains a match
# (at least in the 0th index). Returns -1 if not found.
def listInListIndex(valueList, searchList):
    for index in range(0, len(searchList)):
        if (searchList[index][0][0] == valueList[0]):
            if (searchList[index][0][1] == valueList[1]):
                if (searchList[index][0][2] == valueList[2]):
                    return index

    return -1 # Default if not in list code

def aStar3D(inMap, inX, inY, inLayer, finX, finY, openList, closedList):
    # Calculated coordinates of connected nodes
    thisNode = [inX, inY, inLayer]
    forwardX = calForwardX(inX, inLayer)
    forwardY = calForwardY(inY, inLayer)
    leftLayer = calcCCAngle(inLayer)
    rightLayer = calcCAngle()
    forwardNode = [forwardX, forwardY, inLayer]
    leftNode = [inX, inY, leftLayer]
    rightNode = [inX, inY, rightLayer]

    # Different movement costs can be altered here
    forwardCost = 1
    # This line can be uncommented to add additional cost
    # to diagonal movements, because diagonals will all be
    # odd rather than even.
    #forwardCost = 1 + ((inLayer % 2) * 1.4)
    turnCost = 1

    # Calc adjacent heuristics
    thisCost = distanceHeuristic(inX, inY, finX, finY)
    leftCostEst = turnCost + thisCost
    rightCostEst = leftCostEst
    forwardCostEst = forwardCost + distanceHeuristic(forwardX, forwardY, finX, finY)


    # Calculate list entries
    # First item is this coordinate as a list.
    # Second is the H cost. (Distance from end node)
    # Third is the F cost. (Distance from starting node)
    # Forth is the preceding node as a list.
    ###
    # Check if this is the first recursive call
    if listInListIndex(thisNode, openList) == -1:
        openList.append(thisNode, thisCost, 0, thisNode)
    thisIndex = listInListIndex(thisNode, openList)
    previousNode = openList[thisIndex][3]
    travelCost = openList[thisIndex][2]
    thisList = [thisNode, thisCost, travelCost, previousNode]

    # Check if adjacent nodes are in open or closed list
    leftIndex = listInListIndex(leftNode, openList)
    rightIndex = listInListIndex(rightNode, openList)
    forwardIndex = listInListIndex(forwardNode, openList)
    # Add to openlist if it hasn't
    if leftIndex == -1 and listInListIndex(leftNode, closedList) == -1:
        openList.append([leftNode, leftCostEst - (travelCost + turnCost), travelCost + turnCost, thisNode])
    elif (openList[leftIndex][1] + openList[leftIndex][2] > leftCostEst):
        openList[leftIndex][2] = turnCost + travelCost
    if rightIndex == -1 and listInListIndex(rightNode, closedList) == -1:
        openList.append([rightNode, rightCostEst - (travelCost + turnCost), travelCost + turnCost, thisNode])
    elif (openList[rightIndex][1] + openList[rightIndex][2] > rightCostEst):
        openList[rightIndex][2] = turnCost + travelCost
    if forwardIndex == -1 and inMap[forwardX][forwardY] == 10 and listInListIndex(forwardNode, closedList) == -1:
        openList.append([forwardNode, forwardCostEst - (travelCost + forwardCost), travelCost + forwardCost, thisNode])
    elif (openList[forwardIndex][1] + openList[forwardIndex][2] > forwardCostEst):
        openList[forwardIndex][2] = forwardCost + travelCost

    # Update openlist to remove this node and add it to closed node.
    closedList.append(thisList)
    del openList[listInListIndex(thisNode, openList)]

    # Process the rest of the openlist
    if(inX == finX and inY == finY):
        # Found the route
        return True
    while (len(openList) > 0):
        minIndex = 0
        minLength = openList[0][1] + openList[0][2]
        for index in range(0, len(openList), 1):
            if (openList[0][1] + openList[0][2] > minLength):
                minLength = openList[0][1] + openList[0][2]
                minIndex = index
        # recursively call this function
        if (aStar3D(inMap, openList[minIndex][0][0], openList[minIndex][0][1], openList[minIndex][0][2], \
           finX, finY, openList, closedList) == True):
            return True

    # This search didn't find anything. The route may be unreachable.
    return False

# Return codes:
# 0 - Do nothing
# 1 - Move forward
# 2 - Turn counter-clockwise
# 3 - Turn Clockwise
# -1 - Error or no path
def algPathfind(inMap, initX, initY, initLayer, finalX, finalY):
    simpleMap = bem.SimplifiedMap(inMap.getMap())

    # TODO: Remove once testing is finished
    finalX = 0
    finalY = 0

    finalLayer = 0

    # TODO: Replace once testing is finished
    initX = 0
    initY = 0
    initLayer = 0

    openList = []
    closedList = []
    moveList = []
    if(aStar3D(simpleMap, initX, initY, initLayer, finalX, finalY, openList, closedList) == False):
        # In this case, there was no route
        return -1

    # Grab final angle of path
    finalLayer = closedList[-1][0][3]

    # Reassemble the route to find the first step, starting at the final one
    thisIndex = -1
    previousIndex = 0
    # Checks if any items in a list of lists contains a match
    # (at least in the 0th index). Returns -1 if not found.
    for index in range(0, len(closedList)):
        if (closedList[index][0][0] == finalX):
            if (closedList[index][0][1] == finalY):
                if (closedList[index][0][2] == finalLayer):
                    tempX = closedList[index][0][0]
                    tempY = closedList[index][0][1]
                    tempLayer = closedList[index][0][2]
                    for inIndex in range(0, len(closedList)):
                        if (closedList[inIndex][0][0] == tempX):
                            if (closedList[inIndex][0][1] == tempY):
                                if (closedList[inIndex][0][2] == tempLayer):
                                    if (inIndex == thisIndex):
                                        return convertMovement(initX, initY, initLayer, finalX, finalY, finalLayer)
                                    finalX = tempX
                                    finalY = tempY
                                    finalLayer = tempLayer
                                    previousIndex = thisIndex
                                    thisIndex = inIndex

        return -1  # Default if not in list code

    return 0

if __name__ == '__main__':
    pass