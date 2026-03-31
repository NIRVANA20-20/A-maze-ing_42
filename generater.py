import random
from collections import deque
from parser import Parser

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"N": True, "E": True, "S": True, "W": True}
        self.visited = False
        self.is_42 = False

    def open_wall(self, derection):
        if derection in self.walls:
            self.walls[derection] = False

    def to_hex(self):
        bit_map = ["N", "E", "S", "W"]
        value = 0
        for i, pos in enumerate(bit_map):
            if self.walls[pos] == True:
                value |= 1 << i
        return value

    def __repr__(self):
        return f"Cell({self.x},{self.y})"


class Maze:

    _instance = None
    _is_ins = 0

    def __new__(cls, width, height, entry, exit):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, width, height, entry, exit_m):
        if Maze._is_ins == 0:
            self.width = width
            self.height = height
            self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
            self.entry = entry
            self.exit = exit_m
            self.is_42_map()
            Maze._is_ins = 1

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return 0

    def is_42_map(self):

        if self.width >= 9 and self.height >= 8:
            c_x, c_y = int(self.width / 2), int(self.height / 2)
            map_42 = [
                (c_x - 1, c_y),
                (c_x - 2, c_y),
                (c_x - 3, c_y),
                (c_x + 1, c_y),
                (c_x + 2, c_y),
                (c_x + 3, c_y),
                (c_x - 1, c_y + 1),
                (c_x - 1, c_y + 2),
                (c_x + 1, c_y + 1),
                (c_x + 1, c_y + 2),
                (c_x + 2, c_y + 2),
                (c_x + 3, c_y + 2),
                (c_x - 3, c_y - 1),
                (c_x - 3, c_y - 2),
                (c_x + 3, c_y - 1),
                (c_x + 3, c_y - 2),
                (c_x + 1, c_y - 2),
                (c_x + 2, c_y - 2),
            ]
            for grid in self.grid:
                for cell in grid:
                    x, y = cell.x, cell.y
                    cor = (x, y)
                    if cor in map_42:
                        cell.is_42 = True

    def get_neighbors(self, x, y):

        axis_n = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

        axis = []
        for n in axis_n:
            r, c = n
            cell = self.get_cell(r, c)
            if cell != 0 and cell.visited == False and cell.is_42 == False:
                axis.append(cell)
        return axis

    def convertor(self):
        try:
            entry = str(f"{self.entry}")
            exit = str(f"{self.exit}")
            return entry, exit
        except Exception as e:
            print(e)


class MazeGenerator:
    def __init__(self, maze):
        self.stack = []
        self.maze = maze

    @staticmethod
    def dfs_open_wall(cell, random_cell):
        x, y = cell.x, cell.y
        x1, y1 = random_cell.x, random_cell.y

        if x == x1:
            if y > y1:
                random_cell.open_wall("S")
                cell.open_wall("N")

            else:
                random_cell.open_wall("N")
                cell.open_wall("S")
        if y == y1:
            if x > x1:
                random_cell.open_wall("E")
                cell.open_wall("W")
            else:
                random_cell.open_wall("W")
                cell.open_wall("E")

    def dfs_generator(self):
        x = 0
        y = 0
        stack_cell, maze_generate = self.stack, self.maze
        start = maze_generate.get_cell(x, y)
        start.visited = True
        stack_cell.append(start)
        while stack_cell:
            cell = stack_cell[-1]
            x, y = cell.x, cell.y
            neighbors = maze_generate.get_neighbors(x, y)
            if len(neighbors) == 0:
                stack_cell.pop()
            else:
                cell_r = random.choice(neighbors)
                cell_r.visited = True
                MazeGenerator.dfs_open_wall(cell, cell_r)
                stack_cell.append(cell_r)

    def write_to_file(self):
        maze = self.maze
        list_grid = maze.grid
        self.dfs_generator()
        parsed_file = Parser()
        parsed_file.read_config()
        file = open(parsed_file.file_name, "w")
        print(parsed_file.file_name)
        for grid in list_grid:
            column = ""
            for cell in grid:
                column += hex(cell.to_hex())[2:]
            column += "\n"
            file.write(column)
        file.close()


class MazeSolver:

    path = []
    def __init__(self, maze):
        self.maze = maze


    def bfs_solver(self, start, end):
        queue = deque([start])
        visited = {start}
        parent = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                return self.get_path(parent, start, end)

            cell = self.maze.get_cell(x, y)

            directions = {
                "N": (x, y - 1),
                "E": (x + 1, y),
                "S": (x, y + 1),
                "W": (x - 1, y),
            }

            for d, (nx, ny) in directions.items():
                if cell.walls[d] == False:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        return []

    def get_path(self, parent, start, end):

        path = []
        current = end

        while current != start:
            path.append(current)
            current = parent[current]

        path.append(start)
        path.reverse()

        return path