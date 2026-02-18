
import random

import curses

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False
        self.is_42 = False

    def open_wall(self, derection):
        if derection in self.walls:
            self.walls[derection] = False

    def to_hex(self) :
        bit_map = ['W', 'S', 'E', 'N']
        print(list(enumerate(bit_map)))
        value = 0
        for i, direction in enumerate(bit_map):
            if self.walls[direction] == True:
                value |= (1 << i)
        return value

    def __repr__(self):
        return f"Cell({self.x},{self.y})"

class Maze:
    def __init__(self, width, height, entry, exit_m):
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = [
        [Cell(x, y) for x in range(width)]
        for y in range(height)]
        self.entry = entry
        self.exit = exit_m

    def get_cell(self, x, y):
        if 0 <= x < self.width and  0 <= y < self.height:
            return self.grid[x][y]
        return 0

    def get_neighbors(self, x, y):
        if self.get_cell(x, y) == 0:
            return 0
        axis_n = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
        axis = []
        for n in axis_n:
            r, m = n
            cell = self.get_cell(r, m)
            if cell != 0 and cell.visited == False:
                axis.append(self.get_cell(r, m))
        return axis


class MazeGenerator:
    def __init__(self, maze_m):
        self.stack = []
        self.maze = maze_m

    @staticmethod
    def dfs_open_wall(cell, random_cell):
        x, y = cell.x, cell.y
        x1, y1 = random_cell.x, random_cell.y
        if y == y1:
            if x > x1:
                random_cell.open_wall('E')
                cell.open_wall('W')
            else:
                random_cell.open_wall('W')
                cell.open_wall('E')
        if x == x1:
            if y > y1:
                random_cell.open_wall('S')
                cell.open_wall('N')
            else:
                random_cell.open_wall('N')
                cell.open_wall('S') 


    def dfs_generator(self):
        x = 0
        y = 0 
        stack_cell,  maze_generate  = self.stack, self.maze
        start = maze_generate.get_cell(x,y)
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
        file = open("output_maze.txt", 'w')
        for cell in list_grid:
            column = ""
            for wall in cell:
                column += hex(wall.to_hex())[2:]
            column += '\n'
            file.write(column)
        file.close()


if __name__ == "__main__":
    maz = Maze(3,3,(0,0),(9,9))
    gene = MazeGenerator(maz)
    gene.write_to_file()
