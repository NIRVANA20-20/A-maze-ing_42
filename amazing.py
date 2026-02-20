from mlx.mlx import Mlx

from cell import Cell, Maze

import sys

import time

def kill_it(key, _):
    if key == 65507:
        mlx.mlx_loop_exit(mlx_ptr) 


class Image:
    def __init__(self, mlx: Mlx, mlx_ptr, width, height):
        self.width = width
        self.height = height
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        self.buffer, self.bpp, self.sl, self.format = mlx.mlx_get_data_addr(self.ptr)

    def put_pixel(self, x: int, y: int, color: int):
        offset = int((y * self.sl) + (x * (self.bpp // 8)))
        self.buffer[offset: offset + 4] = color.to_bytes(4, "little")
        

mlx = Mlx()
mlx_ptr = Mlx.mlx_init(mlx)
mlx_wind = Mlx.mlx_new_window(mlx, mlx_ptr, 1440, 1440, "kary00s")

img1 = Image(mlx, mlx_ptr, int(1220), int(1220))
for y in range(1220):
    for x in range(1220):
        img1.put_pixel(x, y, 0xbfbfbfff)

class Generator_maze:
    
    
    def __init__(self, cell_h: int, cell_w: int, cell_border: int):
        self.cell_h = cell_h
        self.cell_w = cell_w       
        self.cell_border = cell_border
        self.cell_height = cell_h
        self.cell_width = cell_w
        self.start_h = 0 ###
        self.start_w = 0 ###
        
    
    def put_north( x, y):

        start_h = y * cell_h + 10
        start_w = x * cell_w + 10
        cell_width = cell_w * (x + 1) + 10
        for y in range(start_h, cell_border + start_h):
            for x in range(start_w, cell_width + cell_border ):
                img1.put_pixel(x, y, 0xFADDD4FF)

    def put_west(x, y):

        start_h = y * cell_h + 10
        start_w = x * cell_w + 10
        cell_height = cell_h * (y + 1) + 10
        for x in range(start_w , start_w + cell_border):
            for y in range(start_h, cell_height):
                img1.put_pixel(x, y, 0xFADDD4FF)

    def put_south(x, y):
        start_h = y * cell_h + 10
        start_w = cell_w * x + 10
        cell_width = cell_w * (x + 1) +10   
        for x in range(start_w ,cell_width):
            for y in range(start_h + cell_h, cell_border +cell_h+ start_h): #########
                img1.put_pixel(x, y,  0xFADDD4FF)

    def put_east(x, y):
        

        start_h = y * cell_h + 10
        start_w = cell_w * (x + 1) + 10
        cell_height = cell_h * (y + 1) + 10
        for x in range(start_w, start_w + cell_border):
            for y in range(start_h, cell_height + cell_border):
                img1.put_pixel(x, y,  0xFADDD4FF)
    

# north border


maze = Maze(50, 50, (0,0), (29,29))

grids =  maze.grid


cell_h = 1200 // 50

cell_w = 1200 // 50

cell_border = 5
start_h = 0
start_w = 0


for cells in grids:
    for cell in cells:
        x, y = cell.x, cell.y
        Generator_maze.put_north(x, y)
        Generator_maze.put_west(x, y)
        Generator_maze.put_east(x, y)
        Generator_maze.put_south(x, y)







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
