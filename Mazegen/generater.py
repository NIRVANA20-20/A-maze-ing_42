import random
from collections import deque
from typing import Any, Tuple


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
            if self.walls[pos] is True:
                value |= 1 << i
        return value

    def __repr__(self):
        return f"Cell({self.x},{self.y})"


class DfsGenerator:
    def __init__(self, width, height, seed, perfect) -> None:
        self.stack = []
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect

    def get_cell(self, x, y, grid):
        if 0 <= x < self.width and 0 <= y < self.height:
            return grid[y][x]
        return None

    def get_neighbors(self, x, y, grid):
        axis_n = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        axis = []
        for n in axis_n:
            r, c = n
            cell = self.get_cell(r, c, grid)
            if cell and cell.visited is False and cell.is_42 is False:
                axis.append(cell)
        return axis

    def generate(self, grid) -> None:
        self.is_42_map(grid)
        random.seed(self.seed)
        x = 0
        y = 0
        start = grid[y][x]
        start.visited = True
        self.stack.append(start)
        while self.stack:
            cell = self.stack[-1]
            x, y = cell.x, cell.y
            neighbors = self.get_neighbors(x, y, grid)
            if len(neighbors) == 0:
                self.stack.pop()
            else:
                cell_r = random.choice(neighbors)
                cell_r.visited = True
                if self.perfect:
                    self.dfs_open_wall_perfect(cell, cell_r)
                else:
                    if x == cell_r.x:
                        self.open_wall_inperfect(cell, grid[y][x - 1], cell_r)
                    else:
                        self.open_wall_inperfect(cell, grid[y - 1][x], cell_r)
                self.stack.append(cell_r)

    def open_wall_perfect(self, cell, random_cell):
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

    def open_wall_inperfect(self, cell, neighbors_cell, random_cell):
        x, y = cell.x, cell.y
        x1, y1 = random_cell.x, random_cell.y

        if x == x1:
            if y > y1:
                random_cell.open_wall("S")
                cell.open_wall("N")
            else:
                random_cell.open_wall("N")
                cell.open_wall("S")
                if y == 0 and x != 0:
                    cell.open_wall("W")
                    neighbors_cell.open_wall("E")
        if y == y1:
            if x > x1:
                random_cell.open_wall("E")
                cell.open_wall("W")
            else:
                random_cell.open_wall("W")
                cell.open_wall("E")
                if x == 0 and y != 0:
                    cell.open_wall("N")
                    neighbors_cell.open_wall("S")

    def is_42_map(self, grid):

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
            for row in grid:
                for cell in row:
                    x, y = cell.x, cell.y
                    cor = (x, y)
                    if cor in map_42:
                        cell.is_42 = True


class MazeSolver:

    def __init__(self, entry: Tuple[int, int], exit: Tuple[int, int], path):
        self.entry = entry
        self.exit = exit
        self.path = path
        self.queue: deque = deque()

    def generate(self, grid) -> None:
        queue: deque = deque([self.entry])
        visited = {self.entry}
        parent = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.exit:
                self.get_path(parent, self.entry, self.exit)
                return
            cell = grid[y][x]
            directions = {
                "N": (x, y - 1),
                "E": (x + 1, y),
                "S": (x, y + 1),
                "W": (x - 1, y),
            }
            for d, (nx, ny) in directions.items():
                if cell.walls[d] is False:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

    def get_path(self, parent, start, end) -> Any:
        current = end
        while current != start:
            self.path.append(current)
            current = parent[current]
        self.path.append(start)
        self.path.reverse()


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        m_entry: Tuple[int, int],
        m_exit: Tuple[int, int],
        seed: int,
        perfect: bool,
        file_name: str,
    ):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.file_name = file_name
        self.generator_algo = DfsGenerator(
            self.width, self.height, self.seed, self.perfect
        )
        self.set_grid()
        self.path = []
        self.path_str = []
        self.entry = m_entry
        self.exit = m_exit
        self.solver = MazeSolver(self.entry, self.exit, self.path)

    def set_grid(self):
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.generator_algo.is_42_map(self.grid)
        return self

    def generate(self):
        self.set_grid()
        self.path.clear()
        self.path_str.clear()
        self.generator_algo.generate(self.grid)
        self.solver.generate(self.grid)
        self.path_filler()
        self.write_to_file()

    def path_filler(self):
        i = 0
        path = self.path
        while i < len(self.path) - 1:
            destination = MazeGenerator.path_checker(path[i], path[i + 1])
            self.path_str.append(destination)
            i += 1

    def path_checker(curr_cell, next_cell):
        x, y = curr_cell
        xn, yn = next_cell
        bit_map = ["N", "E", "S", "W"]
        if x - xn > 0:
            return bit_map[3]
        if x - xn < 0:
            return bit_map[1]
        if y - yn > 0:
            return bit_map[0]
        if y - yn < 0:
            return bit_map[2]

    def write_to_file(self):
        file = open(self.file_name, "w")
        for grid in self.grid:
            column = ""
            for cell in grid:
                column += hex(cell.to_hex())[2:]
            column += "\n"
            file.write(column)

        file.write(f"\n\n{self.entry[0]}, {self.entry[1]}")
        file.write(f"\n{self.exit[0]}, {self.exit[1]}")
        path = "".join(self.path_str)
        file.write(f"\n{path}")

        file.close()
