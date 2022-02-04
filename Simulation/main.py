import birdsEyeMap as bem
import cameraDrones as cd
import sys
import numpy as np
import droneSimulation as sim

testarray = np.array([],np.int16)
testarray2 = np.array([[4, 5, 7, 9], [5, 6,2, 5], [1, 7, 2, 9], [1, 5, 9, 8]], np.int16)
testarray3 = np.array([[5, 4], [3, 2]], np.int16)


print(testarray)
print(testarray2)

#testarray2.append(testarray)

print(testarray2)

print(sys.getsizeof(testarray3[0]))

testarray4 = np.copy(testarray3.astype('int16'))
print(len(testarray4))

mapTest = bem.DroneMap(testarray2)

print(mapTest.getMap())



dronetest = cd.DroneFlying(0, 0, 1)

dronetest.addMap(testarray2)

print(dronetest.getCameraMap())
print(dronetest.getXPos())

simulationTest = sim.Simulation(testarray2)
simulationTest.addBlankMap(2,2)
simulationTest.addAggregateMap(testarray2)
#simulationTest.addFlyingCamera()
#simulationTest.addFlyingMap(testarray3, 0)
simulationTest.printSimulation()

#for x in arraytest