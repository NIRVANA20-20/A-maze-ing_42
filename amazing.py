
from mlx.mlx import Mlx

from cell import Cell, Maze

import sys
import math
import time

def kill_it(key, _):
    if key == 65507:
        mlx.mlx_loop_exit(mlx_ptr) 



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
        

class Generator_maze: 
    def __init__(self, img, maze, mlx):
        self.img = img
        self.maze = maze
        self.cell_b = 5
   
    @staticmethod
    def put_north(x, y, cell_dim, cell_b, img):
        start_h = y * cell_dim
        start_w = x * cell_dim
        cell_width = cell_dim * (x + 1)
        for y in range(start_h, cell_b + start_h):
            for x in range(start_w, cell_width + cell_b):
                img.put_pixel(x, y, 0xFADDD4FF)

    @staticmethod
    def put_west(x, y, cell_dim, cell_b, img):
        start_h = y * cell_dim
        start_w = x * cell_dim 
        cell_height = cell_dim * (y + 1)
        for x in range(start_w , start_w + cell_b):
            for y in range(start_h, cell_height):
                img.put_pixel(x, y, 0xFADDD4FF)

    @staticmethod
    def put_south(x, y, cell_dim, cell_b, img):
        start_h = y * cell_dim
        start_w = cell_dim * x
        cell_width = cell_dim * (x + 1)
        for x in range(start_w ,cell_width):
            for y in range(start_h + cell_dim, cell_b + cell_dim + start_h): #########
                img.put_pixel(x, y,  0xFADDD4FF)

    @staticmethod
    def put_east(x, y, cell_dim, cell_b, img):
        start_h = y * cell_dim
        start_w = cell_dim * (x + 1)
        cell_height = cell_dim * (y + 1)
        for x in range(start_w, start_w + cell_b):
            for y in range(start_h, cell_height + cell_b):
                img.put_pixel(x, y,  0xFADDD4FF)
    
    def creat_cells(self):
        img = self.img
        cell_b = self.cell_b
        val, screen_w, screen_h = mlx.mlx_get_screen_size(img.mlx_ptr)
        min_screen = min(img.width, img.height)
        max_cell = max(self.maze.width, self.maze.height)
        cell_dim = min_screen // max_cell
        print(cell_dim)
        grid = self.maze.grid
        for cells in grid:
            for cell in cells:
                x, y = cell.x, cell.y
                Generator_maze.put_north(x, y, cell_dim, cell_b, img)
                Generator_maze.put_west(x, y, cell_dim, cell_b, img)
                Generator_maze.put_east(x, y, cell_dim, cell_b, img)
                Generator_maze.put_south(x, y, cell_dim, cell_b, img)


# north border

mlx = Mlx()
mlx_ptr = Mlx.mlx_init(mlx)
mlx_wind = Mlx.mlx_new_window(mlx, mlx_ptr, 1440, 1440, "kary00s")

img1 = Image(mlx, mlx_ptr, 1440, 1440)
for y in range(1440):
    for x in range(1440):
        img1.put_pixel(x, y, 0xbfbfbfff)



maze = Maze(10, 20, (0,0), (29,29))
border = Generator_maze(img1, maze, mlx)
border.creat_cells()










mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img1.ptr, 10, 10)


"""

def generator(x, y, color):    
    img1 = Image(mlx, mlx_ptr, int(x), int(y))
    if (x - 5) % 72 == 0:
        print(f"lolo{x,y}")
    else:
        print(f" diiis {x,y}")
    for y in range(img1.height):
        x = 0
        for x in range(img1.width):
            img1.put_pixel(x, y, color)
    return img1

class Cell(Image):
    def __init__(self, height, width):
        self.height = height / 5
        self.width = width / 5



    def north_wall(self):
        for y in range(self.height):
            for x in range(self.width):
                self.put_pixel(x, y, 0xFF035476)        

def draw_square(x, y,size,color):

    i = 0;
    while i < size:
        j = 0;
        while j < size:
            put_pixel(x + i, y + j, color);
            j += 1;
        i += 1;

def display():
    i = 720 // 10
    while i <= 720:
        j = 720 // 10
        while j <= 720:
            img1 = generator(i ,j , 0xFFFFFFFF)
            mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img1.ptr, i, j) 
            img1 = generator(i + 5 , j + 5, 0xFFFF0000)
            j += 720 // 10 
        i += 720 // 10
    mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img1.ptr, i + 5, j + 5)


display()


#draw_square(50, 50, 30, 0xFF0000);





"""

mlx.mlx_key_hook(mlx_wind, kill_it, None)
mlx.mlx_loop(mlx_ptr)
