# collaborative-drones

### Contributors:
* Sharome Burton
* Kuwin Wyke
* Shanae Edwards
* Caleb Sneath
* Micah-Lyn Scotland
* Aquella Warner

![image](/pics/collaborative-drones-banner.png)

## Summary

The aim of this project is to design a robust network of ground-based and air-based autonomous vehicles capable of efficiently and reliably accomplishing an array of pseudo-intelligent tasks, including path-finding, obstacle avoidance, and collaborative problem-solving.

The vehicles, or robots, that form the heart of this project will be two small four-wheeled robots (ground) and one quadcopter (air). Both ground and air vehicles will be equipped with optical cameras in order to accept visual data from the environment and will be controlled using small, hobby-grade Raspberry Pi microcomputers. The network that this project aims to design is one in which the air-based vehicle will track the area of operation of the two ground-based robots, providing a top-down view of the field, revealing the geospatial locations of any possible obstacles, resources, or other points of interest. A top-down view of the entire landscape provides significantly more information about the area than just a first-person view from the perspective of the ground-based robots. The goal is to have the air-based vehicle communicate the information from this top-down view to the ground robots in order to facilitate the solving of the specific problem on the ground. 

A specific problem, for example, will take the form of the need to navigate to a goal destination on the field that is outside of the view of the ground-based robots. Using the information from the top-down view of the air-based robots, the ground robots may drive past obstacles on the field to the goal destination. 

Another example problem would be the case where there is the need for the ground-based robots to collaborate in order to escape a locked room where the exit door is actuated using a button (pressure tile) on the ground within the room, and another button outside of the room. With the knowledge of the location of both buttons from the top-down view, the aim is for the ground-based robots to learn to work together to solve this problem. Ideally, one robot would drive on top of the button, opening the exit door, which would allow the other robot to escape the room. The robot outside the room would then drive onto the exterior exit button, opening the door, allowing the remaining trapped robot to escape.

This project will aim to develop this network by first creating a simple simulation environment for the two ground-based robots with a top-down view (visualize the robots as pieces moving on a chess board or Pac-Man moving through the maze). This simulation environment would be used for the researchers to first solve these path-finding or obstacle avoidance problems by writing or applying algorithms on their own (e.g. Dijkstra’s shortest path algorithm). Using this same simulation environment, the researchers may then apply a form of machine learning called reinforcement learning to train artificial intelligence (A.I.) agents to navigate these problems on their own at an acceptable level of efficiency. The goal is to place these trained A.I. agents in the real-world ground robots so that they may replicate their problem-solving capabilities in the real-world environment.

