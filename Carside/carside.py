# Note: run as python3 carside.py "car number"
# Ex.  python3 carside.py 1
import sys
import socket
import movement as mv

def forward(inCar):
    inCar.moveForward()
def backward(inCar):
    inCar.moveBackward()
def clockwise(inCar):
    inCar.turnClockwise()
def cClockwise(inCar):
    inCar.turnCClockwise()


if __name__ == '__main__':
    carNumber = 1
    # Check if the car number was specified by commandline
    if len(sys.argv) > 1:
        try:
            carNumber = int(sys.argv[1])
        except:
            pass

    thisCar = mv.CarMovement()

    # Load movement dictionary
    # Each movement function will correspond to
    # a specific movement code
    commandDict = {1: forward, 2: backward, 3: clockwise, 4: cClockwise}

    print(str(carNumber))
    commandDict[1](thisCar)

    # Configure message format and source
    headLength = 5
    portNumber = 1093
    try:
        configName = "config" + str(carNumber) + ".txt"
        conFile = open(configName,'r')
        # First line of config file is port
        portNumber = conFile.read()
        portNumber = int(conFile.read())
        conFile.close()
    except:
        portNumber = 1093 # No config file found, use default ports
    inSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inSocket.connect(('10.20.27.193', portNumber))


    while True:
        inCommandFull = ''
        newCommand = True
        while True:
            inCommandPart = inSocket.recv(10)
            if newCommand:
                realLength = int(inCommandPart[:headLength])
                newCommand = False

            inCommandFull += inCommandPart.decode("utf-8")

            # Reset the command reader and call the correct
            # movement functions on transmission end
            if len(inCommandFull)-headLength == realLength:
                try:
                    commandDict[inCommandFull[headLength:]](thisCar)
                    print(str(inCommandFull[headLength:]))
                except:
                    pass
                newCommand = True