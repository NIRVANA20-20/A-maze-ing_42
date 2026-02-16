from mlx.mlx import Mlx

import sys

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
        offset = int((y * self.sl) + (x * (self.bpp / 8)))
        self.buffer[offset: offset + 4] = color.to_bytes(4, "little")
        

mlx = Mlx()
mlx_ptr = Mlx.mlx_init(mlx)
mlx_wind = Mlx.mlx_new_window(mlx, mlx_ptr, 1440, 1440, "kary00s")


img1 = Image(mlx, mlx_ptr, int(1200), int(1200))
for y in range(1200):
    for x in range(1200):
        img1.put_pixel(x, y, 0xFFFFFFFF)

# north border

cell_height = 70
cell_width = 70
cell_border = 10
cell_dim = cell_height + 2 * cell_border
# draw cell 1
for y in range(cell_border):
    for x in range(cell_width + cell_border):
        img1.put_pixel(x, y, 0x0FFFFFFF)

for x in range(cell_border):
    for y in range(cell_height + cell_border):
        img1.put_pixel(x, y, 0x0FFFFFFF)

for y in range(cell_height, cell_height + cell_border):
    for x in range(cell_width + cell_border):
        img1.put_pixel(x, y, 0x0FFFFFFF)

for x in range(cell_width, cell_width + cell_border):
    for y in range(cell_height + cell_border):
        img1.put_pixel(x, y,  0x0FFFFFFF)




mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img1.ptr, 0, 0)

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
