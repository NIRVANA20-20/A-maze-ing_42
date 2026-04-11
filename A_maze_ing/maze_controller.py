from Mazegen.generater import MazeGenerator
from Rendring.rendrer import DrawAnimation, MazeCreator
from Rendring.CellImage import Image
from my_mlx.my_mlx import MyMlx
from themes.themes import Theme
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
        self.is_started = False
        self.is_generated = False
        self.is_solved = False
        self.show = True

    def start(self):
        MyMlx.key_hook(self.call_back, None)

    def maze_cells(self, key: int) -> None:
        if key == Keys.CELLS.value:
            Theme.bg_img_ptr.put_image_to_window()
            self.drawer.generate = False
            self.drawer.is_fin_dfs = False
            self.is_generated = False
            self.is_solved = False
            self.drawer.solve = False
            self.show = True
            self.drawer.is_animation = True
            self.creator.creat_cells()
            self.is_started = True

    def switch_theme(self, key: int) -> None:
        if key == Keys.SWITCH_THEME.value:
            Theme.switch_theme()
            Theme.bg_img_ptr.put_image_to_window()
            self.creator.creat_cells()
            if self.is_generated is True:
                if self.drawer.is_fin_dfs:
                    self.drawer.is_animation = False
                self.drawer.draw_dfs()
            if self.is_solved is True:
                self.drawer.draw()

    def put_maze(self, key: int) -> None:
        if key == Keys.MAZE.value:
            self.generator.generate()
            self.drawer.generate = True
            self.drawer.is_animation = True
            self.is_solved = False
            Theme.bg_img_ptr.put_image_to_window()
            self.creator.creat_cells()
            self.drawer.draw_dfs()
            self.is_generated = True
            self.show = True

    def solve_maze(self, key: int) -> None:
        if key == Keys.SOLVE.value and self.drawer.is_fin_dfs:
            if self.show:
                self.drawer.solve = True
                self.drawer.draw()
                self.is_solved = True
                self.show = False
            else:
                self.drawer.solve = False
                self.creator.creat_cells()
                self.drawer.draw_dfs_no_animation()
                self.show = True

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
