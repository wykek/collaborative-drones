import pygame
import sys
import math
import numpy as np
import droneSimulation as sim
import droneControl as con

class MapUI():
    def __init__(self, inMap = None):
        # Set up fonts
        self.mapFont = pygame.font.SysFont('Corbel', 25)
        self.maxSize = 100

        # Initialize 100X100 empty map if not passed.
        if inMap is None:
            self.__storeMap = np.zeros((100, 100), dtype=np.int16)
        else:
            self.__storeMap = np.copy(inMap.astype('int16'))
    def drawCell(self, cellX, cellY, cellValue, outScreen):
        caption = str(cellValue)
        if cellValue == 0:
            self.textColor = (0, 0.0, 0)
        else:
            self.textColor = (100, 0.0, 100 - 1 * (cellValue % 100))
        renderText = self.mapFont.render(caption, True, self.textColor)

        self.cellColor = (100, 100, 100)
        # Calculate box coordinates
        topLeftX = self.__scaleX * (0.54 * cellX / self.maxSize)
        topLeftY = self.__scaleY * (1.0 * cellY / self.maxSize)
        localWidth = 0.54 * self.__scaleX / self.maxSize
        localHeight = 1.0 * self.__scaleY / self.maxSize
        centerX = topLeftX + (localWidth / 3)
        centerY = topLeftY + 0 * (localHeight / 2)

        # Calculate and draw the rectangle
        localRect = pygame.Rect(int(topLeftX), int(topLeftY),
                                int(localWidth), int(localHeight))
        pygame.draw.rect(outScreen, self.cellColor, localRect)

        # Draw the rectangle
        outScreen.blit(renderText, (int(centerX), int(centerY)))

    def drawMap(self, outScreen):
        mapWidth, mapHeight = np.shape(self.__storeMap)
        tempMax = max(mapWidth, mapHeight)
        if self.maxSize != tempMax:
            self.maxSize = tempMax
            self.setScale(self.__scaleX, self.__scaleY)
        for outIndex in reversed(range(0, mapWidth)):
            for inIndex in reversed(range(0, mapHeight)):
                self.drawCell(outIndex, inIndex, \
                         self.__storeMap[outIndex, inIndex], outScreen)
    def cycleMap(self, outScreen, inMap = None):
        # Initialize 100X100 empty map if not passed.
        if inMap is None:
            self.__storeMap = np.zeros((100, 100), dtype=np.int16)
        else:
            self.__storeMap = np.copy(inMap.astype('int16'))

        # Do the drawing now that its safe
        self.drawMap(outScreen)
    def setScale(self, inX, inY):
        self.__scaleX = inX
        self.__scaleY = inY
        # Scale font, at least 1 point
        minScale = max(min(inX * math.log(100 / self.maxSize, 2), \
                           inY * math.log(self.maxSize, 2)), 400)
        self.mapFont = pygame.font.SysFont('Corbel', int(minScale / 50))
    def setMap(self, inMap):
        self.__storeMap = np.copy(inMap.astype('int16'))


class Button():
    def __init__(self, inCaption = ""):
        # Generate text and font
        self.buttonFont = pygame.font.SysFont('Corbel', 25)
        self.textColor = (0, 0, 0)
        self.caption = inCaption
        self.renderText = self.buttonFont.render(self.caption, \
        True, self.textColor)

        self.topLeftX = None
        self.topLeftY = None
        self.width = None
        self.height = None
        self.scaleX = None
        self.scaleY = None
        # 0 is not hover, not clicked, 1 is hover but
        # not clicked, 2 is clicking
        self.clickState = 0
        # Gray
        self.color = (180, 180, 180)
        self.onClickColor = (150, 150, 225)
        self.onHoverColor = (150, 150, 150)
        self.onReleaseColor = (120, 120, 120)

        self.validPosition = False
        self.rect = None
    def setPosition(self, inTopLeftX, inTopLeftY, inWidth, \
    inHeight):
        self.topLeftX = inTopLeftX
        self.topLeftY = inTopLeftY
        self.width =  inWidth
        self.height = inHeight
        self.validPosition = True
    def setScale(self, inX, inY):
        self.scaleX = inX
        self.scaleY = inY

        # Initialize or update rectangle for button
        # if everything needed is known
        if self.validPosition == True:
            self.rect = pygame.Rect(int(self.topLeftX * self.scaleX), \
            int(self.topLeftY * self.scaleY), int(self.width * \
            self.scaleX), int(self.height * self.scaleY))
    def cycleButton(self, mousePos, inClicked, outScreen):

        # clicked previously
        if self.clickState == 2:
            if inClicked == True:
                pygame.draw.rect(outScreen, self.onClickColor, self.rect)
            # User released the click, need to activate button function
            else:
                self.clickState = 1
                pygame.draw.rect(outScreen, self.onReleaseColor, self.rect)
                # This is the only state which returns
                # true, so we print the text here as well before
                # returning.
                outScreen.blit(self.renderText, \
                (int(self.topLeftY * self.scaleX), int(self.topLeftY * \
                self.scaleY)))
                return True
        else:
            # Check if the mouse is within the coordinates of the button.
            if ((self.scaleX * self.topLeftX <= mousePos[0])  and \
            mousePos[0] <= self.scaleX * (self.topLeftX + self.width)\
            and (self.scaleY * self.topLeftY <= mousePos[1])  and \
            mousePos[1] <= self.scaleY * (self.topLeftY + self.height)):
                if inClicked == True:
                    self.clickedState = 2
                    pygame.draw.rect(outScreen, self.onClickColor, self.rect)
                else:
                    self.clickedState = 1
                    pygame.draw.rect(outScreen, self.onHoverColor, self.rect)
            else:
                self.clickState = 0
                pygame.draw.rect(outScreen, self.color, self.rect)

        # Display text and return false, since we reached this point
        outScreen.blit(self.renderText, \
        (int(self.topLeftX * self.scaleX), \
        int(self.topLeftY * self.scaleY)))
        return False

class TextBox():
    def __init__(self, inCaption = ""):
        # Generate text and font
        self.textFont = pygame.font.SysFont('Corbel', 35)
        self.textColor = (0, 0, 0)
        self.caption = inCaption
        self.renderText = self.textFont.render(self.caption, \
        True, self.textColor)

        self.topLeftX = None
        self.topLeftY = None
        self.width = None
        self.height = None
        self.scaleX = None
        self.scaleY = None

        self.validPosition = False
        self.rect = None
    def setPosition(self, inTopLeftX, inTopLeftY, inWidth, \
    inHeight):
        self.topLeftX = inTopLeftX
        self.topLeftY = inTopLeftY
        self.width =  inWidth
        self.height = inHeight
        self.validPosition = True
    def setScale(self, inX, inY):
        self.scaleX = inX
        self.scaleY = inY

        # Initialize or update rectangle for button
        # if everything needed is known
        if self.validPosition == True:
            self.rect = pygame.Rect(int(self.topLeftX * self.scaleX), \
            int(self.topLeftY * self.scaleY), int(self.width * \
            self.scaleX), int(self.height * self.scaleY))
    def cycleText(self, outScreen):
        # Display text
        outScreen.blit(self.renderText, \
        (int(self.topLeftX * self.scaleX), int(self.topLeftY * self.scaleY)))

class SimulationUI:
    def __init__(self, inSim = None):
        if inSim != None:
            self.simulation = inSim
        else:
            self.simulation = sim.Simulation()
            self.simulation.addBlankMap(100, 100)
            self.simulation.addFlyingCamera()
            self.simulation.addFlyingPosition(0, 0, 0, 1)

    def runUI(self):
        # Initialize screen variables
        defaultX = 1280
        defaultY = 720
        pygame.init()
        colorLight = (200, 200, 210)
        simScreen = pygame.display.set_mode((defaultX, defaultY), \
        pygame.RESIZABLE|pygame.DOUBLEBUF)
        pygame.display.set_caption('Collaborative Drones Simulation')
        simScreen.fill(colorLight)

        # Stores if user closed the window or clicks.
        exitFlag = False
        isClicked = False

        # Initialize screen
        simScreen.fill(colorLight)
        pygame.display.flip()

        # Stores functions to iterate over during events
        resizeList = []

        lastWindowX = simScreen.get_width()
        lastWindowY = simScreen.get_height()

        mouseCoords = pygame.mouse.get_pos()

        # Screen Objects initializations
        # Camera Select Area
        # Camera Prompt
        cameraPrompt = TextBox("Camera 1")
        cameraPrompt.setPosition(0.55, 0.1, 0.35, 0.0)
        cameraPrompt.setScale(defaultX, defaultY)
        resizeList.append(cameraPrompt.setScale)
        # Rotate Counter Clockwise
        rotCCButton = Button("Rot CC")
        rotCCButton.setPosition(0.68, 0.1, 0.06, 0.04)
        rotCCButton.setScale(defaultX, defaultY)
        resizeList.append(rotCCButton.setScale)
        # Rotate Clockwise
        rotCButton = Button("Rot CC")
        rotCButton.setPosition(0.75, 0.1, 0.06, 0.04)
        rotCButton.setScale(defaultX, defaultY)
        resizeList.append(rotCButton.setScale)
        # Move Forward
        movCamForButton = Button("Mov For")
        movCamForButton.setPosition(0.82, 0.1, 0.066, 0.04)
        movCamForButton.setScale(defaultX, defaultY)
        resizeList.append(movCamForButton.setScale)
        # Move Back
        movCamBackButton = Button("Mov Bac")
        movCamBackButton.setPosition(0.89, 0.1, 0.068, 0.04)
        movCamBackButton.setScale(defaultX, defaultY)
        resizeList.append(movCamBackButton.setScale)
        # Previous Camera
        prevCamButton = Button("<")
        prevCamButton.setPosition(0.965, 0.1, 0.01, 0.04)
        prevCamButton.setScale(defaultX, defaultY)
        resizeList.append(prevCamButton.setScale)
        # Next Camera
        nextCamButton = Button(">")
        nextCamButton.setPosition(0.98, 0.1, 0.01, 0.04)
        nextCamButton.setScale(defaultX, defaultY)
        resizeList.append(nextCamButton.setScale)
        # MapUI
        self.mapUI = MapUI(self.simulation.getMap())
        resizeList.append(self.mapUI.setScale)

        #Cars
        carPrompts = []
        carRotCCs = []
        carRotCs = []
        carMoveForwards = []
        carMoveBacks = []

        # Iterate through all five car buttons and prompts
        for index in range(0,4):
            # Car Prompts
            carPrompts.append(TextBox("Car " + str(index + 1)))
            carPrompts[index].setPosition\
            (0.55, 0.15 + 0.05 * index, 0.35, 0.0)
            carPrompts[index].setScale(defaultX, defaultY)
            resizeList.append(carPrompts[index].setScale)
            # Car Rotate Counter Clockwise Buttons
            carRotCCs.append(Button("Rot CC"))
            carRotCCs[index].setPosition\
            (0.68, 0.15 + 0.05 * index, 0.06, 0.04)
            carRotCCs[index].setScale(defaultX, defaultY)
            resizeList.append(carRotCCs[index].setScale)
            # Car Rotate Clockwise Buttons
            carRotCs.append(Button("Rot C"))
            carRotCs[index].setPosition\
            (0.75, 0.15 + 0.05 * index, 0.06, 0.04)
            carRotCs[index].setScale(defaultX, defaultY)
            resizeList.append(carRotCs[index].setScale)
            # Car Move Forwards Buttons
            carMoveForwards.append(Button("Mov For"))
            carMoveForwards[index].setPosition\
            (0.82, 0.15 + 0.05 * index, 0.066, 0.04)
            carMoveForwards[index].setScale(defaultX, defaultY)
            resizeList.append(carMoveForwards[index].setScale)
            # Car Move Backwards Buttons
            carMoveBacks.append(Button("Mov Bac"))
            carMoveBacks[index].setPosition\
            (0.89, 0.15 + 0.05 * index, 0.068, 0.04)
            carMoveBacks[index].setScale(defaultX, defaultY)
            resizeList.append(carMoveBacks[index].setScale)
        # Simulation Mode Area
        # Simulation Prompt
        simulationPrompt = TextBox("Simulation Mode")
        simulationPrompt.setPosition(0.55, 0.5, 0.35, 0.0)
        simulationPrompt.setScale(defaultX, defaultY)
        resizeList.append(simulationPrompt.setScale)
        # Manual Simulation Control Method
        manualButton = Button("Manual")
        manualButton.setPosition(0.75, 0.5, 0.06, 0.04)
        manualButton.setScale(defaultX, defaultY)
        resizeList.append(manualButton.setScale)
        # AI 1 (Algorithmic)Button Method
        ai1Button = Button("AI 1")
        ai1Button.setPosition(0.82, 0.5, 0.03, 0.04)
        ai1Button.setScale(defaultX, defaultY)
        resizeList.append(ai1Button.setScale)
        # AI 2 (Machine Learning)Button Method
        ai2Button = Button("AI 2")
        ai2Button.setPosition(0.86, 0.5, 0.03, 0.04)
        ai2Button.setScale(defaultX, defaultY)
        resizeList.append(ai2Button.setScale)
        # Stop AI Button
        stopButton = Button("Stop AI")
        stopButton.setPosition(0.75, 0.55, 0.06, 0.04)
        stopButton.setScale(defaultX, defaultY)
        resizeList.append(stopButton.setScale)
        # Map Select Area
        # Map Source Prompt
        mapPrompt = TextBox("Map Source")
        mapPrompt.setPosition(0.55, 0.6, 0.35, 0.0)
        mapPrompt.setScale(defaultX, defaultY)
        resizeList.append(mapPrompt.setScale)
        # Random Map Button
        randomButton = Button("Random")
        randomButton.setPosition(0.75, 0.6, 0.07, 0.04)
        randomButton.setScale(defaultX, defaultY)
        resizeList.append(randomButton.setScale)
        # Import File Map Button
        fileButton = Button("File")
        fileButton.setPosition(0.83, 0.6, 0.028, 0.04)
        fileButton.setScale(defaultX, defaultY)
        resizeList.append(fileButton.setScale)
        # Import Camera Map Button
        cameraButton = Button("Camera")
        cameraButton.setPosition(0.867, 0.6, 0.063, 0.04)
        cameraButton.setScale(defaultX, defaultY)
        resizeList.append(cameraButton.setScale)
        # mapUI Object
        self.mapUI.setScale(defaultX, defaultY)

        # Window cycle
        while exitFlag is False:
            # Clear the screen from previous frames
            simScreen.fill(colorLight)

            # Check if user closed window
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    exitFlag = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    isClicked = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    isClicked = False

            # Check for window resizes
            newX = simScreen.get_width()
            newY = simScreen.get_height()
            if newX != lastWindowX or newY != lastWindowY:
                lastWindowX = newX
                lastWindowY = newY
                for index in range(0,len(resizeList)):
                    resizeList[index](newX, newY)

            mouseCoords = pygame.mouse.get_pos()

            # Update screen objects and check buttons
            # Camera row
            cameraPrompt.cycleText(simScreen)
            if rotCCButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if rotCButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if movCamForButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if movCamBackButton.cycleButton(mouseCoords, isClicked, \
            simScreen):
                pass
            if prevCamButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if nextCamButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            # Button rows
            for index in range(4):
                carPrompts[index].cycleText(simScreen)
                if carRotCCs[index].cycleButton(mouseCoords, isClicked, simScreen):
                    pass
                if carRotCs[index].cycleButton(mouseCoords, isClicked, simScreen):
                    pass
                if carMoveForwards[index].cycleButton(mouseCoords, isClicked, simScreen):
                    pass
                if carMoveBacks[index].cycleButton(mouseCoords, isClicked, simScreen):
                    pass
            # Simulation mode row
            simulationPrompt.cycleText(simScreen)
            if manualButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if ai1Button.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if ai2Button.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if stopButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            # Map select mode row
            mapPrompt.cycleText(simScreen)
            if randomButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if fileButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            if cameraButton.cycleButton(mouseCoords, isClicked, simScreen):
                pass
            # Update visual MapUI object
            self.mapUI.cycleMap(simScreen, self.simulation.getMap())

            pygame.display.update()
            pygame.display.flip()

        # Exit pygame after quitting.
        pygame.quit()

if __name__ == '__main__':
    testarray = np.array([], np.int16)
    testarray2 = np.array([[4, 5, 7, 9], [5, 6, 2, 5], [1, 7, 2, 9], [1, 5, 9, 8]], np.int16)
    testarray3 = np.array([[5, 4], [3, 2]], np.int16)

    testarray4 = np.array([\
        [4, 5, 7, 9, 16, 12, 83, 13], \
        [5, 6, 2, 5, 12, 10, 2, 8], \
        [1, 0, 2, 9, 2, 4, 8, 1], \
        [1, 5, 9, 8, 7, 7, 3, 20]], \
        np.int16)

    testarray5 = np.zeros((100, 100), dtype=np.int16)

    print(testarray)
    print(testarray2)

    # testarray2.append(testarray)

    print(testarray2)

    print(sys.getsizeof(testarray3[0]))

    print("Here")
    # Drone control test
    #simulationTest = con.Controller(testarray2)
    simulationTest = sim.Simulation(testarray4)
    simulationTest.addCarCamera()
    simulationTest.addCarPosition(1, 1, 1, 4)
    simulationTest.moveCarForward(1)
    print("Here")

    simulationInstance = SimulationUI(simulationTest)
    simulationInstance.runUI()
