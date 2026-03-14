import parsing
from mlx.mlx import Mlx
import random
import os
from generating import Maze, MazeGenerator


def generate_ouput_file():
    width, height, (x_entry, y_entry), (x_exit, y_exit), file_name = (
        parsing.read_config()
    )
    maz = Maze(width, height, (x_entry, y_entry), (x_exit, y_exit))
    generator = MazeGenerator(maz)
    generator.write_to_file()


def call_back(key, _):
    if key == 65507 or key == 65307:
        mlx.mlx_loop_exit(mlx_ptr)
    if key == 65293:
        Theme.switch_theme()
        redrawing(border, maze, 0, Theme.color_bg, Theme.color_42)
    if key == 97:
        Theme.switch_theme()
        redrawing(border, maze, 0, Theme.color_bg, Theme.color_42)
        redrawing(border, maze, 1, Theme.color_bg, Theme.color_42)
    if key == 32:
        generate_ouput_file()
        redrawing(border, maze, 0, Theme.color_bg, Theme.color_42)
        redrawing(border, maze, 1, Theme.color_bg, Theme.color_42)


    print(key)



class Image:
    
    def __init__(self, mlx: Mlx, mlx_ptr, width, height):
        self.width = width
        self.height = height
        self.mlx_ptr = mlx_ptr
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        self.buffer, self.bpp, self.sl, self.format = mlx.mlx_get_data_addr(self.ptr)
    
    @staticmethod
    def put_first_affiche(file_name):
        abs_path = os.path.abspath(".") + "/images/" + file_name
        img, _, _ = mlx.mlx_png_file_to_image(mlx_ptr, abs_path)
        mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img, 0, 200)

    def put_pixel(self, x: int, y: int, color: int):
        offset = int((y * self.sl) + (x * (self.bpp // 8)))
        self.buffer[offset: offset + 4] = color.to_bytes(4, "little")
    
    @staticmethod
    def create_color(r: int, g: int, b: int) -> int:
        col = 0xFF000000 | (r << 16) | (g << 8) | b
        return col

class Theme:
    themes = [
            (Image.create_color(102, 255, 255), Image.create_color(0, 153, 153)),
            (Image.create_color(255, 204, 255), Image.create_color(153, 0, 76)), 
            (Image.create_color(255, 178, 102), Image.create_color(153, 76, 0)), 
            (Image.create_color(224, 224, 224), Image.create_color(64, 64, 64)),
            (Image.create_color(224, 224, 224), Image.create_color(64, 64, 64))
        ] 
    theme_index = 0
    color_bg, color_42 = themes[theme_index]

    @classmethod
    def switch_theme(cls):
        cls.theme_index = (cls.theme_index + 1) % len(cls.themes)
        cls.color_bg, cls.color_42 = cls.themes[cls.theme_index]


class GeneratorMaze:
    def __init__(self, maze, mlx, mlx_ptr):
        self.maze = maze
        self.cell_b = 4

    @staticmethod
    def put_north(x, y, cell_dim, cell_b, cell_br, img, color):
        start_h = y * cell_dim
        start_w = x * cell_dim
        cell_width = cell_dim * (x + 1)
        for y in range(start_h, cell_b + start_h):
            for x in range(start_w + cell_br, cell_width + cell_b - cell_br):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_west(x, y, cell_dim, cell_b, cell_br, img, color):
        start_h = y * cell_dim
        start_w = x * cell_dim
        cell_height = cell_dim * (y + 1)
        for x in range(start_w, start_w + cell_b):
            for y in range(start_h + cell_br, cell_height + cell_b - cell_br):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_south(x, y, cell_dim, cell_b, cell_br, img, color):
        start_h = y * cell_dim
        start_w = cell_dim * x
        cell_width = cell_dim * (x + 1)
        for x in range(start_w + cell_br, cell_width + cell_b - cell_br):
            for y in range(start_h + cell_dim, cell_b + cell_dim + start_h):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_east(x, y, cell_dim, cell_b, cell_br, img, color):
        start_h = y * cell_dim
        start_w = cell_dim * (x + 1)
        cell_height = cell_dim * (y + 1)
        for x in range(start_w, start_w + cell_b):
            for y in range(start_h + cell_br, cell_height + cell_b - cell_br):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_img(img, color):
        for y in range(img.height):
            for x in range(img.width):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_inside(x, y, cell_dim, cell_b, img, color):
        start_h = y * cell_dim
        start_w = x * cell_dim
        cell_width = cell_dim * (x + 1)
        for y in range(start_h + cell_b, cell_dim + start_h + cell_b):
            for x in range(start_w + cell_b, cell_width + cell_b):
                img.put_pixel(x, y, color)

    def creat_cells(self, img, cell_b, cell_dim, color_42, color_bg):
        poss_h = 5
        poss_w = int((window_width - self.maze.width * cell_dim) / 2)
        grid = self.maze.grid

        GeneratorMaze.put_img(img, color_bg)
        for cells in grid:
            for cell in cells:
                x, y = cell.x, cell.y
                if cell.is_42 is True:
                    GeneratorMaze.put_inside(x, y, cell_dim, cell_b, img, color_42)

                else:
                    color = Image.create_color(255, 255, 255)
                    GeneratorMaze.put_north(x, y, cell_dim, cell_b, 0, img, color)
                    GeneratorMaze.put_east(x, y, cell_dim, cell_b, 0, img, color)
                    GeneratorMaze.put_west(x, y, cell_dim, cell_b, 0, img, color)
                    GeneratorMaze.put_south(x, y, cell_dim, cell_b, 0, img, color)
        mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img.ptr, poss_w, poss_h)

    @staticmethod
    def remove_wall_helper(x, y, pos, img, cell_b, cell_dim, color):
        if pos == "N":
            GeneratorMaze.put_north(x, y, cell_dim, cell_b, cell_b, img, color)
        elif pos == "E":
            GeneratorMaze.put_east(x, y, cell_dim, cell_b, cell_b, img, color)
        elif pos == "W":
            GeneratorMaze.put_west(x, y, cell_dim, cell_b, cell_b, img, color)
        elif pos == "S":
            GeneratorMaze.put_south(x, y, cell_dim, cell_b, cell_b, img, color)

    @staticmethod
    def read_from_file(y, flage):
        with open("output_maze.txt", "r") as file:
            rows = file.read().split("\n")
            return rows[y]

    def remove_wall(self, img, cell_b, cell_dim, color, poss_h, poss_w):
        x = 0
        y = 0
        width = self.maze.width
        height = self.maze.height
        bit_map = ["W", "S", "E", "N"]
        while y < height:
            row = GeneratorMaze.read_from_file(y, 1)
            print(row)
            x = 0
            while x < width:
                value_final = format(int(row[x], 16), "04b")
                for i, pos in enumerate(bit_map):
                    if value_final[i] == "0":

                        print(value_final, int(row[x], 16), pos)
                        GeneratorMaze.remove_wall_helper(
                            x, y, pos, img, cell_b, cell_dim, color
                        )
                x += 1
            y += 1
        GeneratorMaze.read_from_file(0, 0)
        mlx.mlx_put_image_to_window(mlx_ptr, mlx_wind, img.ptr, poss_w, poss_h)


def redrawing(border, maze, flage, color_bg, color_42):

    _, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)
    min_screen = min(screen_w, screen_h)
    max_cell = max(maze.width, maze.height)
    cell_dim = int((min_screen / max_cell) * 0.75)
    cell_b = 4
    img_height = int(maze.height * cell_dim + cell_b)
    img_width = int(maze.width * cell_dim + cell_b)
    poss_h = 5
    poss_w = int((window_width - maze.width * cell_dim) / 2)

    img = Image(mlx, mlx_ptr, img_width, img_height)
    if flage == 0:
        border.creat_cells(img, cell_b, cell_dim, color_42, color_bg)
    if flage == 1:
        border.remove_wall(img, cell_b, cell_dim, color_bg, poss_h, poss_w)
if __name__ == "__main__":
    width, height, entry, exit, file_name = parsing.read_config()
    # read_from_file(height, width)
    mlx = Mlx()
    mlx_ptr = Mlx.mlx_init(mlx)
    window_height = 1000
    window_width = 1000
    mlx_wind = Mlx.mlx_new_window(mlx, mlx_ptr, window_width, window_height, "kary00s")
    maze = Maze(width, height, entry, exit)
    maze.is_42_map()
    border = GeneratorMaze(maze, mlx, mlx_ptr)
    
    Image.put_first_affiche("maze_affiche.png")
    mlx.mlx_key_hook(mlx_wind, call_back, None)
    mlx.mlx_loop(mlx_ptr)
