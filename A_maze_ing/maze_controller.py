from Generating.generater import MazeGenerator
from Rendring.rendrer import DrawAnimation, MazeCreator
from Rendring.CellImage import Image
from my_mlx.my_mlx import MyMlx
from themes.themes import Theme
from typing import List
from enum import Enum
import sys


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
        self.is_started = False
        self.is_generated = False
        self.is_solved = False
        self.show = True

    def start(self):
        MyMlx.key_hook(self.call_back, None)

    def maze_cells(self, key: int) -> None:
        if key == Keys.CELLS.value:
            Theme.bg_img_ptr.put_image_to_window()
            self.creator.creat_cells()
            self.is_started = True
            self.is_generated = False
            self.is_solved = False
            self.show = True

    def switch_theme(self, key: int) -> None:
        if key == Keys.SWITCH_THEME.value:
            Theme.switch_theme()
            Theme.bg_img_ptr.put_image_to_window()
            self.creator.creat_cells()
            self.drawer.is_animation = False
            self.show = True
            if self.is_generated is True:
                self.drawer.draw_dfs()
            if self.is_solved is True:
                self.drawer.draw()
                self.show = False

    def put_maze(self, key: int) -> None:
        if key == Keys.MAZE.value:
            self.generator.generate()
            Theme.bg_img_ptr.put_image_to_window()
            self.drawer.is_animation = True
            self.creator.creat_cells()
            self.drawer.draw_dfs()
            self.is_solved = False
            self.is_generated = True
            self.show = True

    def solve_maze(self, key: int) -> None:
        # print(self.is_generated, self.drawer.is_draw, self.show)
        if (
            key == Keys.SOLVE.value
            and self.is_generated is True
            and self.drawer.is_draw is False
            and self.show is True
        ):

            self.drawer.draw()
            self.is_solved = True
            self.show = False
        elif self.show is False:
            self.creator.creat_cells()
            self.drawer.draw_dfs_no_animation()
            self.show = True
        # print(self.is_solved)

    def get_path_string(self) -> List[str]:
        path_list = []
        path = self.solve.path
        for i in range(len(path) - 1):
            destination = DrawAnimation.path_checker(path[i], path[i + i])
            path_list.append(destination)
        return path_list

    def call_back(self, key: int, _) -> None:
        try:
            self.maze_cells(key)
            if self.is_started:
                self.solve_maze(key)
                self.switch_theme(key)
                self.put_maze(key)
            if key == Keys.EXIT.value:
                MyMlx.loop_exit()
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            return
