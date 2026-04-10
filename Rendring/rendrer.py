from my_mlx.my_mlx import MyMlx
from typing import Any
from themes.themes import Theme
from Rendring.CellImage import Image
from Generating.maze import Maze


class MazeCreator:
    def __init__(self):
        self.maze = Maze()
        self.img = Image()
        self.is_put = True

    def creat_cells(self):

        self.img.put_img()
        for cells in self.maze.grid:
            for cell in cells:
                x, y = cell.x, cell.y
                if cell.is_42 is True:
                    self.img.put_inside(x, y)

                else:
                    self.img.put_north(x, y, Theme.border_color)
                    self.img.put_east(x, y, Theme.border_color)
                    self.img.put_west(x, y, Theme.border_color)
                    self.img.put_south(x, y, Theme.border_color)
        if self.is_put is True:
            MyMlx.put_image_to_window(self.img.ptr, self.img.poss_w, self.img.poss_h)

    def remove_wall_helper(self, x, y, pos):
        if pos == "N":
            self.img.put_north(x, y, Theme.bg_color, self.img.cell_b)
        elif pos == "E":
            self.img.put_east(x, y, Theme.bg_color, self.img.cell_b)
        elif pos == "W":
            self.img.put_west(x, y, Theme.bg_color, self.img.cell_b)
        elif pos == "S":
            self.img.put_south(x, y, Theme.bg_color, self.img.cell_b)

    def read_from_file(self, y):
        with open(self.maze.file_name, "r") as file:
            rows = file.read().split("\n")
            return rows[y]

    @staticmethod
    def check_binary(value):
        bit_map = ["W", "S", "E", "N"]
        return_pos = []
        for i, pos in enumerate(bit_map):
            if value[i] == "0":
                return_pos.append(pos)
        return return_pos


class DrawAnimation:
    def __init__(self):
        self.maze = Maze()
        self.creator = MazeCreator()
        self.img = Image()
        self.color = Theme.bg_color
        self.path = self.maze.path
        self.is_animation = True
        self.is_draw = True

    def draw_entry_exit(self):
        x_entry, y_entry = self.maze.entry
        x_exit, y_exit = self.maze.exit
        self.img.put_entry_exit(x_entry, y_entry)
        self.img.put_entry_exit(x_exit, y_exit)

    def draw(self):
        self.i = 0
        self.draw_entry_exit()
        MyMlx.loop_hook(self.bfs_loop_hook, None)
        print("walid")

    def draw_dfs(self):
        self.x = 0
        self.y = 0
        if self.is_animation is False:
            self.draw_dfs_no_animation()
        else:
            MyMlx.loop_hook(self.dfs_loop_hook, None)

    @staticmethod
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

    def bfs_loop_hook(self, _):
        if self.i + 1 == len(self.path):
            return
        destination = DrawAnimation.path_checker(
            self.path[self.i], self.path[self.i + 1]
        )
        x, y = self.path[self.i]
        self.img.put_path(x, y, destination)
        MyMlx.put_image_to_window(self.img.ptr, self.img.poss_w, self.img.poss_h)
        self.i += 1

    def dfs_loop_hook(self, _):
        try:
            width = self.maze.width
            height = self.maze.height
            if self.x == width:
                self.x = 0
                self.y += 1

            if self.y == height:
                if self.is_animation is False:
                    MyMlx.put_image_to_window(
                        self.img.ptr, self.img.poss_w, self.img.poss_h
                    )
                self.is_draw = False
                return

            if self.x < width:
                row = self.creator.read_from_file(self.y)
                value = format(int(row[self.x], 16), "04b")
                pos_list = MazeCreator.check_binary(value)
                for pos in pos_list:
                    self.creator.remove_wall_helper(self.x, self.y, pos)
                if self.is_animation is True:
                    MyMlx.put_image_to_window(
                        self.img.ptr, self.img.poss_w, self.img.poss_h
                    )
            self.x += 1
        except Exception as e:
            print(e)

    def draw_dfs_no_animation(self):
        width = self.maze.width
        height = self.maze.height
        for x in range(width):
            for y in range(height):
                row = self.creator.read_from_file(y)
                value = format(int(row[x], 16), "04b")
                pos_list = MazeCreator.check_binary(value)
                for pos in pos_list:
                    self.creator.remove_wall_helper(x, y, pos)
        MyMlx.put_image_to_window(self.img.ptr, self.img.poss_w, self.img.poss_h)

    def draw_path(self, path: Any) -> None:
        pass
