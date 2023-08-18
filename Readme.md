# Warehouse Simulator with Resource Sharing

## Introduction

This document outlines the proposed features of the Warehouse Simulator, a system that employs smart resource sharing among robots to efficiently achieve goals even when certain modules fail. The simulator demonstrates the utilization of resource sharing among rovers tasked with transporting colored polygons to designated drop locations based on color and shape criteria.

The simulation environment consists of movable obstacles, rovers, RGB polygons of various shapes, and drop location racks.

## Prerequisites

- Python 3.6 or later
- Pygame
- Matplotlib

## Running the Simulator

1. Ensure you have Python 3.6 or later installed on your system.
2. Install the required dependencies by running the following command in your terminal:

   ```
   pip install pygame matplotlib
   ```

3. Clone or download the repository containing the Warehouse Simulator source code.

4. Navigate to the repository directory using your terminal.

5. Run the simulator by executing the `main.py` script:

   ```
   python main.py
   ```

6. Follow the on-screen instructions to interact with the simulator and observe the robots' resource sharing behaviors.


## Modules

### 1. Path Planning

The robots possess an initial understanding of object drop locations and the positions of other rovers. As rovers traverse the environment, unexplored areas are updated and shared among all robots. Path planning involves selecting the shortest route between pickup and drop locations.

**Fail Safe:**
- If path planning fails, predefined paths will be used until an obstacle is encountered.
- In case of movement failure, the area will be marked as an obstacle and updated globally.
- Near conveyor belts, the robotic arm will be employed to handle polygons for nearby robots.

### 2. Communication

Robots share global and local variables to exchange environment details and module statuses. If a robot module fails, nearby robots take proactive actions.

**Fail Safe:**
- If communication module fails, the nearest robot approaches the last known location to check for halting.
- A halted robot prompts the location as an obstacle.
- A polygon-free robot retrieves polygons from the failed robot.
- Upon recovery, the robot updates both local and global variables to account for offline changes.

### 3. RGB Module

The RGB sensor detects polygon colors, determining suitable drop locations based on color assignments.

**Fail Safe:**
- Robots without RGB information wait at the pickup location, guided by sensor-equipped robots to identify polygon color and appropriate drop locations.

### 4. Robot Arm

The robot's arm facilitates polygon pickup and drop-off on varying racks.

**Fail Safe:**
- If the robot's arm fails, other robots handle polygon transfers from the carrier to the conveyor belt.

### 5. Collision Avoidance

This module detects obstacles, adapting path planning and global variables accordingly. Objects may be relocated during simulation, necessitating continuous scanning.

**Fail Safe:**
- In case of collision avoidance detector failure, the rover halts and requests the nearest robot for assistance in navigating around obstacles.

## Conclusion and Results

The Warehouse Simulator with Resource Sharing emphasizes the importance of communication in resource optimization. The results will compare successful attempts per unit time with and without inter-rover communication, accounting for random module failures. The analysis aims to showcase the benefits of resource sharing in enhancing swarm robot productivity, minimizing resource and time losses due to unexpected malfunctions.

