This project has been created as part of the 42 curriculum by **kanahiz**, **olaizi**.
# A-maze-ing
## Description

A-Maze-ing is an interactive 2D maze generator and solver that provides real-time visualization using a custom-built MLX wrapper. The project focuses on generating mazes, displaying their construction step by step, and solving them using graph traversal algorithms.

The main objective is to explore different maze generation techniques, visualize their behavior, and compute the shortest path between two points using an efficient solving algorithm.


## Instructions
#### Requirements

Python 3.8 or higher
MLX shared library (mlx/libmlx.so)
System dependencies for MLX (SDL2 / X11 on Linux)
Build & Run

Using Makefile:

- make intall
- make run
- make lint
- make clean

## Configuration

The program expects a configuration file as its only argument.

Full Configuration Format
- WIDTH=20
- HEIGHT=20
- ENTRY=0,0
- EXIT=19,19
- SEED=22
- OUTPUT_FILE=maze.txt
- PERFECT=False

#### Parameters Description
- WIDTH / HEIGHT: Dimensions of the maze (must be > 0)
ENTRY: Starting position (format: x,y)
- EXIT: Ending position (format: x,y)
- SEED: Controls randomness for reproducibility
- OUTPUT_FILE: File where results are saved
- PERFECT: Defines whether the maze has no - loops (True/False)
Important Notes
- A reserved “42” area appears in the center for larger mazes
- ENTRY and EXIT must not be placed inside this reserved zone
- Invalid configurations will terminate execution with an error

## Usage
Controls
- Enter → Start maze generation
- space → Generate using DFS
- P     → Solve using BFS
- p     → Show/Hide solution path
- C     → Change visual theme
- Esc   → Exit program
Output Format

#### The generated file contains:

- Maze grid (line by line)
- Empty line
- Entry coordinates (x,y)
- Exit coordinates (x,y)
- Shortest path computed by BFS

Maze Generation Algorithm
Implemented Algorithms
Depth-First Search (recursive backtracking)

DFS is efficient and easy to implement, producing long and visually clear corridors.
Using BFS allows comparison between deterministic structure (DFS) 

#### Features
Dynamic theme switching
Visualization of both generation and solving processes 

Several parts of the project are modular and reusable:

- MLX Wrapper (mlx/, my_mlx/)
Abstracts low-level graphics handling and simplifies rendering

- Parser (Parsing/parser.py)
Generic key-value configuration parser usable in other projects
- Controlling Model (maze.py/, maze_controller.py)
ogic and state management
- Mazegen (generater.py)
Clean separation of generation and solving strategies
Reusable Maze Package

- The mazegen module provides a standalone maze generator:

- Central class: MazeGenerator
Supports DFS generation + BFS solving
Produces both in-memory results and output files
Usage Concept

- Create instance with parameters
Call generation method
Retrieve maze or solution
mazegen Package

- A minimal and reusable Python module for maze generation.

## Installation
pip install mazegen-1.0.0-py3-none-any.whl
#### Team 

olaizi: 
        - algorithm implementation, maze generation logic, 
        - BFS solver Initial phase: basic DFS generator with simple rendering integration of BFS solver

kanahiz: 
        - rendering system, MLX integration, Parsnig
        - visualization Planning & Evolution


- Project Structure

```
A-Maze-ing/
├── a_maze_ing.py
├── config.txt
├── Makefile
├── controlling/
| └── maze_controller.py
| └── maze.py
|
|
├── Mazegen/
| └── generater.py
| └── pyproject.toml
|
|
├── my_mlx/
| └── mlx/
| └── my_mlx.py
|
|
├── Parsing/
| └── parser.py
|
├── Rendering/
| └── render.py
| └── CellImage.py
|
└── Themes/
  └── themes.py


```
## Resources
- I created a summary for this project that includes all the necessary information and the knowledge I gained [click_here](https://www.tldraw.com/f/Fj3Di-nkFnyd3mZdtsP2y?d=v-981.-1358.5842.6228.page)
- MLX documentation
- [Depth-First Search (DFS) references](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/)
- [Breadth-First Search (BFS) tutorials](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)
## AI Usage

- AI tools were used to assist with:

   - Structuring and organizing the README
   - Improving clarity and wording of documentation
   - Refining explanations for algorithms and architecture
   - readme Generating

All implementation logic, algorithms, and design decisions were developed by the team.