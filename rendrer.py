from parser import Parser
import os
from generater import Maze, MazeGenerator, MazeSolver
from my_mlx import MyMlx

def generate_ouput_file(flage: int)-> list:
    _, _, entry, exit, _, _= Parser.read_config()
    maze = Maze(0, 0, 0, 0) 

    if flage == 0:
        generator = MazeGenerator(maze)
        generator.dfs_generator()
        generator.write_to_file() 
    if flage == 1:
        solve = MazeSolver(maze)
        return solve.bfs_solver(entry, exit)
    
def call_back(key, _):
    if key == 65507 or key == 65307:
        MyMlx.loop_exit()
    if key == 65293:
        Theme.switch_theme()
        Image.put_bg_affiche("affiche_ban.png", 0, 200)
        redrawing(0, Theme.color_bg, Theme.color_42, 0)
    if key == 99:
        Theme.switch_theme()
        redrawing(0, Theme.color_bg, Theme.color_42, 0)
        redrawing(1, Theme.color_bg, Theme.color_42, 0)
    if key == 112:
        path = generate_ouput_file(1)
        redrawing(2, Theme.color_bg, Theme.color_42, path)
    if key == 32:
        generate_ouput_file(0)
        redrawing(1, Theme.color_bg, Theme.color_42, 0)

class Image:
    _instance = None
    _is_ins = 0

    def __new__(cls,width, height):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, width, height):
        if Image._is_ins == 0:
            self.width = width
            self.height = height
            self.ptr = MyMlx.new_image(width, height)
            self.buffer, self.bpp, self.sl, self.format = MyMlx.get_data_addr(self.ptr)
            for y in range(height):
                for x in range(width):
                    self.put_pixel(x, y, 0x0000000)
            Image._is_ins = 1

    @staticmethod
    def put_bg_affiche(file_name, x, y):
        abs_path = os.path.abspath(".") + "/images/" + file_name
        img, _, _ = MyMlx.png_file_to_image(abs_path)
        MyMlx.put_image_to_window(img, x, y)

    def put_pixel(self, x: int, y: int, color: int):
        offset = int((y * self.sl) + (x * (self.bpp // 8)))
        self.buffer[offset : offset + 4] = color.to_bytes(4, "little")

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
        (Image.create_color(224, 224, 224), Image.create_color(64, 64, 64)),
    ]
    theme_index = 0
    color_bg, color_42 = themes[theme_index]

    @classmethod
    def switch_theme(cls):
        cls.theme_index = (cls.theme_index + 1) % len(cls.themes)
        cls.color_bg, cls.color_42 = cls.themes[cls.theme_index]

class MazeCreator:
    def __init__(self, maze, cell_dim):
        self.maze = maze
        self.cell_b = 4
        img_height = int(maze.height * cell_dim + self.cell_b)
        img_width = int(maze.width * cell_dim + self.cell_b)
        self.img = Image(img_width, img_height)

    @staticmethod
    def get_dim_pos(maze):
        min_screen = min(MyMlx.screen_width, MyMlx.screen_height)
        max_cell = max(maze.width, maze.height)
        cell_dim = int((min_screen / max_cell) * 0.75)
        pos_w = int((2000 - maze.width * cell_dim) / 2)
        pos_h = 5
        return cell_dim, pos_w, pos_h
    
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
        start_h = y * cell_dim + cell_b
        start_w = x * cell_dim
        cell_width = cell_dim * (x + 1)
        for y in range(start_h, cell_dim + start_h ):
            for x in range(start_w + cell_b, cell_width + cell_b):
                img.put_pixel(x, y, color)

    @staticmethod
    def put_path(x, y, cell_dim, destination, img, color):
        start_h = y * cell_dim + (cell_dim // 3)
        start_w = x * cell_dim + (cell_dim // 3)

        if destination == "N":
            for y in range(start_h - cell_dim,  start_h):
                for x in range(start_w, start_w + (cell_dim // 3)):
                    img.put_pixel(x, y, color)

        elif destination == "S":
            for y in range(start_h, (cell_dim // 3) + cell_dim + start_h):
                for x in range(start_w, start_w + (cell_dim // 3)):
                    img.put_pixel(x, y, color)

        elif destination == "E":
            for y in range(start_h, start_h + cell_dim // 3):
                for x in range(start_w, start_w + cell_dim + cell_dim // 3):
                    img.put_pixel(x, y, color)

        elif destination == "W":
            for y in range(start_h, start_h + cell_dim // 3):
                for x in range(start_w - cell_dim, start_w):
                    img.put_pixel(x, y, color)

    def creat_cells(self, cell_b, cell_dim, color_42, color_bg):
        poss_h = 5
        poss_w = int((2000 - self.maze.width * cell_dim) / 2)
        grid = self.maze.grid
        img = self.img

        MazeCreator.put_img(img, color_bg)
        for cells in grid:
            for cell in cells:
                x, y = cell.x, cell.y
                if cell.is_42 is True:
                    MazeCreator.put_inside(x, y, cell_dim, cell_b, img, color_42)

                else:
                    color = Image.create_color(255, 255, 255)
                    MazeCreator.put_north(x, y, cell_dim, cell_b, 0, img, color)
                    MazeCreator.put_east(x, y, cell_dim, cell_b, 0, img, color)
                    MazeCreator.put_west(x, y, cell_dim, cell_b, 0, img, color)
                    MazeCreator.put_south(x, y, cell_dim, cell_b, 0, img, color)

        MyMlx.put_image_to_window(img.ptr, poss_w, poss_h)

    @staticmethod
    def remove_wall_helper(x, y, pos, img, cell_b, cell_dim, color):
        if pos == "N":
            MazeCreator.put_north(x, y, cell_dim, cell_b, cell_b, img, color)
        elif pos == "E":
            MazeCreator.put_east(x, y, cell_dim, cell_b, cell_b, img, color)
        elif pos == "W":
            MazeCreator.put_west(x, y, cell_dim, cell_b, cell_b, img, color)
        elif pos == "S":
            MazeCreator.put_south(x, y, cell_dim, cell_b, cell_b, img, color)

    @staticmethod
    def read_from_file(y, flag):
        with open("output_maze.txt", "r") as file:
            rows = file.read().split("\n")
            return rows[y]

    def remove_wall(self, cell_b, cell_dim, color, poss_h, poss_w):
        x = 0
        y = 0
        img = self.img
        width = self.maze.width
        height = self.maze.height
        bit_map = ["W", "S", "E", "N"]
        while y < height:
            row = MazeCreator.read_from_file(y, 1)
            x = 0
            while x < width:
                value_final = format(int(row[x], 16), "04b")
                for i, pos in enumerate(bit_map):
                    if value_final[i] == "0":
                        MazeCreator.remove_wall_helper(
                            x, y, pos, img, cell_b, cell_dim, color
                        )
                x += 1
            y += 1
        MazeCreator.read_from_file(0, 0)
        MyMlx.put_image_to_window(img.ptr, poss_w, poss_h)

class DrawAnimation:
    def __init__(self, path, maze):

        self.cell_dim, self.pos_w, self.pos_h = MazeCreator.get_dim_pos(maze)
        self.img = Image(0, 0)
        self.mlx_ptr = MyMlx.mlx_ptr
        self.win_ptr = MyMlx.win_ptr
        self.path = path
        self.i = 0
    
    def draw_entry_exit(self, entry, exit):
        x_entry, y_entry = entry
        x_exit, y_exit = exit
        MazeCreator.put_inside(x_entry, y_entry, self.cell_dim, 4, self.img, Theme.color_42)
        MazeCreator.put_inside(x_exit, y_exit, self.cell_dim, 4, self.img, Theme.color_42)

    def draw(self):
        MyMlx.loop_hook(self.loop_hook, None)
    
    @staticmethod
    def path_checker(curr_cell , next_cell):
        x ,y = curr_cell
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
            destination = DrawAnimation.path_checker(self.path[self.i], self.path[self.i + 1])
            x, y = self.path[self.i]
            MazeCreator.put_path(x, y, self.cell_dim, destination, self.img, Theme.color_42)
            MyMlx.put_image_to_window(self.img.ptr, self.pos_w, self.pos_h)
            self.i += 1
        except Exception as e:
            print(e)


def redrawing(flag, color_bg, color_42, path):

    width, height, entry, exit, _, _= Parser.read_config()
    maze = Maze(width, height, entry, exit) 
    cell_dim, pos_w, pos_h = MazeCreator.get_dim_pos(maze)

    border = MazeCreator(maze, cell_dim)
    if flag == 0:
        border.creat_cells(4, cell_dim, color_42, color_bg)
    if flag == 1:
        border.remove_wall(4, cell_dim, color_bg, pos_h, pos_w)
    if flag == 2:
        path_list = []
        for i in range(len(path) - 1):
            destination = DrawAnimation.path_checker(path[i], path[i+1])
            path_list.append(destination)
        path_drawer = DrawAnimation(path, maze)
        path_drawer.draw_entry_exit(entry, exit)
        path_drawer.draw()
        
if __name__ == "__main__":
    Image.put_bg_affiche("maze_affiche.png", 0, 200)
    MyMlx.key_hook(call_back, None)
    MyMlx.loop()
