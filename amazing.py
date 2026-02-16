from mlx.mlx import Mlx

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
mlx_wind = Mlx.mlx_new_window(mlx, mlx_ptr, 1200, 1000, "kary00s")
mlx.mlx_key_hook(mlx_wind, kill_it, None)

def generator():    
    img1 = Image(mlx, mlx_ptr, 720, 720)
    for y in range(img1.height):
        for x in range(img1.width):
            img1.put_pixel(x, y, 0xFF432595)
    return img1

class Cell(Image):
    def __init__(self, height, width):
        self.height = height / 5
        self.width = width / 5

    def north_wall(self):
        for y in range(self.height):
            for x in range(self.width):
                self.put_pixel(x, y, 0xFF035476)        


img1 = generator()

mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img1.ptr, 250, 150)

mlx.mlx_loop(mlx_ptr)