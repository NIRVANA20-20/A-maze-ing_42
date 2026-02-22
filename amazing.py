
from mlx.mlx import Mlx

from cell import Cell, Maze

import sys
import math
import time

def call_back(key, _):
    if key == 65507 or key == 65307:
        mlx.mlx_loop_exit(mlx_ptr) 
    if key == 99:
        Image.switch_color()


class Image:
    def __init__(self, mlx: Mlx, mlx_ptr, width, height):
        self.width = width
        self.height = height
        self.mlx_ptr = mlx_ptr
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        self.buffer, self.bpp, self.sl, self.format = mlx.mlx_get_data_addr(self.ptr)

    def put_pixel(self, x: int, y: int, color: int):
        offset = int((y * self.sl) + (x * (self.bpp // 8)))
        self.buffer[offset: offset + 4] = color.to_bytes(4, "little")


    def create_color(r: int, g: int, b: int) -> int:
        col = 0xFF000000 | (r << 16) | (g << 8) | b
        return col

    # def switch_color():
    #     r = 0
    #     g = 100
    #     b = 200
    #     Image.create_color(r, g, b)


class Generator_maze: 
    def __init__(self, maze, mlx, mlx_ptr):
        self.maze = maze
        self.cell_b = 4

    @staticmethod
    def put_north(x, y, cell_dim, cell_b, img, color):
        start_h = y * cell_dim
        start_w = x * cell_dim
        cell_width = cell_dim * (x + 1)
        for y in range(start_h, cell_b + start_h):
            for x in range(start_w, cell_width + cell_b):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_west(x, y, cell_dim, cell_b, img, color):
        start_h = y * cell_dim
        start_w = x * cell_dim 
        cell_height = cell_dim * (y + 1)
        for x in range(start_w , start_w + cell_b):
            for y in range(start_h, cell_height):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_south(x, y, cell_dim, cell_b, img, color):
        start_h = y * cell_dim
        start_w = cell_dim * x
        cell_width = cell_dim * (x + 1)
        for x in range(start_w ,cell_width):
            for y in range(start_h + cell_dim, cell_b + cell_dim + start_h):
                img.put_pixel(x, y,  color)

    @staticmethod
    def put_east(x, y, cell_dim, cell_b, img, color):
        start_h = y * cell_dim
        start_w = cell_dim * (x + 1)
        cell_height = cell_dim * (y + 1)
        for x in range(start_w, start_w + cell_b):
            for y in range(start_h, cell_height + cell_b):
                img.put_pixel(x, y,  color)

    @staticmethod
    def put_img(img):
        for y in range(img.height):
            for x in range(img.width):
                img.put_pixel(x, y, Image.create_color(155, 53, 0))
    @staticmethod
    def put_inside(x, y, cell_dim, cell_b, img, color):
        start_h = y * cell_dim
        start_w = x * cell_dim 
        cell_width = cell_dim * (x + 1)
        for y in range(start_h + cell_b, cell_dim + start_h + cell_b):
            for x in range(start_w + cell_b, cell_width + cell_b):
                img.put_pixel(x, y, color)



    
    def creat_cells(self):

        _, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)

        min_screen = min(screen_w, screen_h)
        max_cell = max(self.maze.width, self.maze.height)
        cell_dim = int((min_screen / max_cell) * 0.75)
        cell_b = 4
        img_height = int(self.maze.height * cell_dim + cell_b)
        img_width = int(self.maze.width * cell_dim + cell_b)
        img = Image(mlx, mlx_ptr, img_width, img_height)

        poss_h = int((1000 - self.maze.height * cell_dim) / 2)
        poss_w = int((1000 - self.maze.width * cell_dim) / 2)

        Generator_maze.put_img(img)
        grid = self.maze.grid

        for cells in grid:
            for cell in cells:
                x, y = cell.x, cell.y
                if cell.is_42 == True:
                    color = Image.create_color(255, 128, 0)
                    Generator_maze.put_inside(x, y, cell_dim, cell_b, img, color)

                else:
                    color = Image.create_color(0, 0, 0)
                    Generator_maze.put_north(x, y, cell_dim, cell_b, img, color)
                    Generator_maze.put_east(x, y, cell_dim, cell_b, img, color)
                    Generator_maze.put_west(x, y, cell_dim, cell_b, img, color)
                    Generator_maze.put_south(x, y, cell_dim, cell_b, img, color)
    
        mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img.ptr, poss_w, poss_h)




mlx = Mlx()
mlx_ptr = Mlx.mlx_init(mlx)
mlx_wind = Mlx.mlx_new_window(mlx, mlx_ptr, 1000, 1000, "kary00s")



maze = Maze(24, 24, (0,0), (0,0))
border = Generator_maze(maze, mlx, mlx_ptr)



border.creat_cells()


mlx.mlx_key_hook(mlx_wind, call_back, None)
mlx.mlx_loop(mlx_ptr)
