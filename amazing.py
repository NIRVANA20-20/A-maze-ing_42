from parser import Parser
from generater import Maze,  MazeGenerator, MazeSolver
from my_mlx import MyMlx
from enum import Enum
from rendrer import Image, DrawAnimation, MazeCreator, Theme


class Keys(Enum):
    EXIT = 65507
    CELLS = 65293
    SWITCH_THEME = 99
    SOLVE = 112
    MAZE = 32


def redrawing(flag, color_bg, color_42, path):

    file_parsed = Parser()
    file_parsed.read_config()
    width, height, entry, exit, _ , _ = file_parsed.get_infos()
    maze = Maze(width, height, entry, exit) 
    cell_dim, _, _ = MazeCreator.get_dim_pos(maze)
    border = MazeCreator(maze, cell_dim)
    drawer = DrawAnimation(path, color_bg)

    if flag == 0:
        border.creat_cells(color_42, color_bg)
    if flag == 1:
        drawer.draw_dfs()
    if flag == 2:
        path_list = []
        for i in range(len(path) - 1):
            destination = DrawAnimation.path_checker(path[i], path[i+1])
            path_list.append(destination)
        drawer.draw_entry_exit(entry, exit)
        drawer.draw()


def generate_ouput_file(flage: int)-> list:
    file_parsed = Parser()
    file_parsed.read_config()
    _, _, entry, exit, _, _= file_parsed.get_infos()
    maze = Maze(0, 0, 0, 0) 
    generator = MazeGenerator(maze)

    if flage == 0:
        generator.dfs_generator()
        generator.write_to_file() 
    if flage == 1:
        solve = MazeSolver(maze)
        return solve.bfs_solver(entry, exit)


def call_back(key, _):

    match key:
        case Keys.EXIT.value:
            MyMlx.loop_exit()

        case Keys.CELLS.value:
            Theme.switch_theme()
            
            Image.put_bg_affiche(Theme.bg_img, 0, 0)
            redrawing(0, Theme.color_bg, Theme.color_42, 0)

        case Keys.SWITCH_THEME.value:
            Theme.switch_theme()
            Image.put_bg_affiche(Theme.bg_img, 0, 0)
            redrawing(0, Theme.color_bg, Theme.color_42, 0)
            redrawing(1, Theme.color_bg, Theme.color_42, 0)

        case Keys.SOLVE.value:
            path = generate_ouput_file(1)
            redrawing(2, Theme.color_bg, Theme.color_42, path)

        case Keys.MAZE.value:
            generate_ouput_file(0)
            Image.put_bg_affiche(Theme.bg_img, 0, 0)
            redrawing(0, Theme.color_bg, Theme.color_42, 0)
            redrawing(1, Theme.color_bg, Theme.color_42, 0)


if __name__ == "__main__":
    Image.put_bg_affiche("main_affiche.png", 0, 0)
    MyMlx.key_hook(call_back, None)
    MyMlx.loop()
