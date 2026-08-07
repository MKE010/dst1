Overview
This repository contains the source code for a terminal-based pathfinding game developed as a final course assignment. The project simulates a routing problem within a weighted graph environment, where the player must navigate from a randomized starting node to a designated safe zone (Node V) while avoiding an actively pursuing enemy.

The primary objective of this project is the practical application of fundamental data structures and graph traversal algorithms in a functional software environment.

Custom Data Structures
To adhere to strict project constraints, the use of built-in language structures for core logic was prohibited. The following data structures were implemented manually:

Graph: An undirected, weighted graph representing the map topology (Nodes A-V, 26 edges). It utilizes an adjacency list structure to manage node connections and weights.

Hash Table: Implements separate chaining to handle user authentication. It stores usernames and SHA-256 encrypted passwords securely, preventing duplicate account creation.

Max Heap: Manages the game's leaderboard system. It dynamically sorts and retrieves the highest-scoring players in real-time after every match.

Stack: Facilitates the game's "Undo" mechanic, pushing and popping the game state (player position, enemy position, and current score) to allow the player to revert decisions with a point penalty.

Pathfinding Algorithms
The core gameplay loop relies on two distinct traversal algorithms to dictate movement:

Dijkstra's Algorithm: Calculates the absolute shortest weighted path from the player's current position to the goal. Based on the specific routing requirements and map constraints of this assignment, Dijkstra was prioritized over A* to ensure accurate and uncompromised edge weight resolution.

Breadth-First Search (BFS): Dictates the enemy's movement logic. When triggered, BFS calculates the shortest unweighted path (fewest number of edges) toward the player's current node to simulate an active pursuit.

Project Architecture
The codebase is modularized to separate the underlying data logic from the game engine and user interface:

main.py - The entry point script to execute the program.

engine.py - Contains the GameEngine class, managing the game loop, turn sequence, and user session data.

algorithms.py - Houses the standalone functions for Dijkstra and BFS graph traversal.

data_structures.py - Contains the manual class definitions for MyStack, H_Table, maxHeap, and graphObj.

utils.py - Contains helper functions for terminal output formatting and screen clearing.

Execution Instructions
This application runs entirely in a command-line interface. To run the project locally:

Ensure Python 3.x is installed on your machine.

Clone this repository or download the source code files into a single directory.

Open a terminal or command prompt and navigate to the project directory.

Execute the following command:

Bash
python main.py
