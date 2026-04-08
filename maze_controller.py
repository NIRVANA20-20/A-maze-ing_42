from generater import MazeGenerator
from rendrer import DrawAnimation, MazeCreator
from CellImage import Image
from my_mlx import MyMlx
from themes import Theme
from typing import List
from enum import Enum


class Keys(Enum):
    EXIT = 65507
    CELLS = 65293
    SWITCH_THEME = 99
    SOLVE = 112
    MAZE = 32


class MazeController:

    def __init__(self, generator: MazeGenerator) -> None:

        self.generator = generator
        self.creator = MazeCreator()
        self.img = Image()
        self.drawer = DrawAnimation()
        self.img.set_dimension(
            generator.width, generator.height
        ).img_ptr().img_data_addr()
        Theme.START.put_image_to_window()
        self.is_start = False
        self.draw = False
        self.is_soved = False

    def start(self):
        MyMlx.key_hook(self.call_back, None)

    def maze_cells(self, key: int) -> None:
        if key == Keys.CELLS.value:
            Theme.switch_theme()
            Theme.bg_img_ptr.put_image_to_window()
            self.creator.is_put = True
            self.creator.creat_cells()
            self.is_start = True
            self.draw = False
            self.is_soved = False

    def switch_theme(self, key: int) -> None:
        if key == Keys.SWITCH_THEME.value:
            Theme.switch_theme()
            Theme.bg_img_ptr.put_image_to_window()
            self.creator.creat_cells()
            self.drawer.is_animation = False
            if self.draw is True:
                self.drawer.draw_dfs()
            if self.is_soved is True:
                self.drawer.draw()

    def put_maze(self, key: int) -> None:
        if key == Keys.MAZE.value:
            self.generator.generate()
            Theme.bg_img_ptr.put_image_to_window()
            self.drawer.is_animation = True
            self.creator.creat_cells()
            self.drawer.draw_dfs()
            self.draw = True
            self.is_soved = False

    def solve_maze(self, key: int) -> None:
        if key == Keys.SOLVE.value:
            self.drawer.draw()
            self.is_soved = True

    def get_path_string(self) -> List[str]:
        path_list = []
        path = self.solve.path
        for i in range(len(path) - 1):
            destination = DrawAnimation.path_checker(path[i], path[i + i])
            path_list.append(destination)
        return path_list

    def call_back(self, key: int, _) -> None:

        self.maze_cells(key)
        print((key))
        if self.is_start:
            self.solve_maze(key)
            self.switch_theme(key)
            self.put_maze(key)
        if key == Keys.EXIT.value:
            MyMlx.loop_exit()
