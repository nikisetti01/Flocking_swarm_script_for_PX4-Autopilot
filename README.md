# 🦜 Flocking-Swarm-Algorithm

This repository contains the code developed for my Bachelor Degree thesis in **Ingegneria Informatica** (105/110). The project focuses on implementing and optimizing a flocking algorithm for a drone swarm using the PX4-Autopilot simulator.

## 📚 Project Overview

### 🛠️ Introduction
The goal of this project is to develop and optimize a flocking algorithm for a swarm of drones. The simulation and testing are performed using the PX4-Autopilot open-source simulator. This project demonstrates the application of swarm intelligence principles to coordinate multiple drones in a simulated environment, aiming for efficient and cohesive flight patterns.

### 🤖 Flocking Algorithm
The core of this project is the **Flocking.py** script, which implements the flocking algorithm for drone swarm coordination. The flocking algorithm is inspired by the behavior of birds and fish, where each drone (agent) adjusts its velocity based on its local neighbors to achieve cohesive movement.

#### Key Parameters:
- **Cohesion**: The tendency of drones to move towards the center of mass of their local neighbors.
- **Alignment**: The tendency of drones to align their direction with the average direction of their neighbors.
- **Separation**: The tendency of drones to maintain a minimum distance from their neighbors to avoid collisions.

### 📈 Performance Analysis
To ensure optimal performance, the flocking algorithm is evaluated and fine-tuned based on several parameters:

1. **Consistency**: Measures how consistently drones maintain the desired flocking behavior.
2. **Coverage**: Assesses how well the swarm covers the simulation area without overlapping or leaving gaps.
3. **Stability**: Evaluates the stability of the swarm formation over time.

### 🧬 Genetic Algorithm for Optimization
To enhance the performance of the flocking algorithm, a **Genetic Algorithm** is employed to optimize the initial parameters of the flocking behavior. This optimization process involves:

1. **Parameter Encoding**: Representing the flocking parameters (cohesion, alignment, separation) as genes in a genetic algorithm.
2. **Fitness Function**: Evaluating the performance of the flocking algorithm based on consistency, coverage, and stability metrics.
3. **Selection, Crossover, and Mutation**: Applying genetic algorithm techniques to evolve the parameters and improve the flocking behavior.

### 🏗️ Implementation
- **Flocking.py**: Contains the implementation of the flocking algorithm and its integration with the PX4-Autopilot simulator.
- **genetic_algorithm.py**: Implements the genetic algorithm to optimize the flocking parameters.

### 🚀 Usage
1. **Setup PX4-Autopilot**: Ensure that the PX4-Autopilot simulator is properly set up and configured on your system.
2. **Run Flocking Algorithm**:
   ```bash
   python Flocking.py
