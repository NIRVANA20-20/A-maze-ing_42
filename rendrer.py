from my_mlx import MyMlx
from typing import Any
from themes import Theme
from CellImage import Image
from generater import MazeGenerator


class MazeCreator:
    def __init__(self, generater):
        self.generater = generater
        self.img = Image()

    def creat_cells(self):

        self.img.img_put_pixel()
        for cells in self.generater.grid:
            for cell in cells:
                x, y = cell.x, cell.y
                if cell.is_42 is True:
                    self.img.put_inside(x, y)

                else:
                    self.img.put_north(x, y)
                    self.img.put_east(x, y)
                    self.img.put_west(x, y)
                    self.img.put_south(x, y)

        MyMlx.put_image_to_window(self.img.ptr, self.img.poss_w, self.img.poss_h)

    def remove_wall_helper(self, x, y, pos):
        if pos == "N":
            self.img.put_north(x, y, self.img.cell_b)
        elif pos == "E":
            self.img.put_east(x, y, self.img.cell_b)
        elif pos == "W":
            self.img.put_west(x, y, self.img.cell_b)
        elif pos == "S":
            self.img.put_south(x, y, self.img.cell_b)

    def read_from_file(self, y):
        with open(self.generater.file_name, "r") as file:
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
    def __init__(self, generater):
        self.generater = generater
        self.creator = MazeCreator(generater)
        self.img = Image()
        self.color = Theme.bg_color
        self.i = 0
        self.x = 0
        self.y = 0

    def draw_entry_exit(self):
        x_entry, y_entry = self.entry
        x_exit, y_exit = exit
        self.img.put_inside(x_entry, y_entry)
        self.img.put_inside(x_exit, y_exit)

    def draw(self):
        MyMlx.loop_hook(self.loop_hook, None)

    def draw_dfs(self):
        MyMlx.loop_hook(self.loop_hook2, None)

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

    def loop_hook(self, _):
        try:
            if self.i + 1 == len(self.path):
                return
            destination = DrawAnimation.path_checker(
                self.path[self.i], self.path[self.i + 1]
            )
            x, y = self.path[self.i]
            self.img.put_path(x, y)
            MyMlx.put_image_to_window(self.img.ptr, self.pos_w, self.pos_h)
            self.i += 1
        except Exception as e:
            print(e)

    def loop_hook2(self, _):
        try:
            width = self.generater.width
            height = self.generater.height
            if self.x == width:
                self.x = 0
                self.y += 1

            if self.y == height:
                return

            if self.x < width:
                row = self.creator.read_from_file(self.y)
                value = format(int(row[self.x], 16), "04b")
                pos_list = MazeCreator.check_binary(value)
                for pos in pos_list:
                    self.creator.remove_wall_helper(self.x, self.y, pos)
                MyMlx.put_image_to_window(
                    self.img.ptr, self.img.poss_w, self.img.poss_h
                )
            self.x += 1
        except Exception as e:
            print(e)

    def draw_path(self, path: Any) -> None:
        pass
