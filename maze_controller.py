from generater import Maze, MazeSolver, MazeGenerator
from my_mlx import MyMlx
from rendrer import Image, DrawAnimation, MazeCreator, Theme
from enum import Enum
from typing import List


class Keys(Enum):
    EXIT = 65507
    CELLS = 65293
    SWITCH_THEME = 99
    SOLVE = 112
    MAZE = 32


class MazeController:

    def __init__(self, generator: MazeGenerator) -> None:

        self.is_start = False
        self.maze = Maze()
        self.generator = generator
        self.drawer = DrawAnimation()

    def start(self):
        MyMlx.key_hook(self.call_back, None)

    def maze_cells(self, key: int) -> None:
        if key == Keys.CELLS.value:
            Theme.switch_theme()
            Image.put_bg_affiche(Theme.bg_img, 0, 0)
            self.border.creat_cells(Theme.color_42, Theme.color_bg)
            self.is_start = True

    def switch_theme(self, _: int) -> None:
        Theme.switch_theme()
        Image.put_bg_affiche(Theme.bg_img, 0, 0)
        self.drawer.draw_dfs()

    def put_maze(self, key: int) -> None:
        if key == Keys.MAZE.value:
            self.maze.grid_maze()
            self.generator.generate()
            self.generator.write_to_file()
            Image.put_bg_affiche(Theme.bg_img, 0, 0)
            self.border.creat_cells(Theme.color_42, Theme.color_bg)
            self.drawer.get_path(self.solve.bfs_solver(self.entry_m, self.exit_m))
            self.drawer.draw_dfs()

    def solve_maze(self, key: int) -> None:
        if key == Keys.SOLVE.value:
            if MazeGenerator.is_finished:
                self.drawer.draw_entry_exit(self.entry_m, self.exit_m)
                self.drawer.draw_dfs()

    def get_path_string(self) -> List[str]:
        path_list = []
        path = self.solve.path
        for i in range(len(path) - 1):
            destination = DrawAnimation.path_checker(path[i], path[i + i])
            path_list.append(destination)
        return path_list

    def call_back(self, key: int, _) -> None:

        self.maze_cells(key)
        if self.is_start:
            self.solve_maze(key)
            self.switch_theme(key)
            self.put_maze(key)
        if key == Keys.EXIT.value:
            MyMlx.loop_exit()
