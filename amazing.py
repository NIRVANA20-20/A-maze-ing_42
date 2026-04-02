from parser import Parser
from generater import Maze, MazeGenerator, MazeSolver
from my_mlx import MyMlx
from enum import Enum
from rendrer import Image, Theme, redrawing


class Keys(Enum):
    EXIT = 65507
    CELLS = 65293
    SWITCH_THEME = 99
    SOLVE = 112
    MAZE = 32
    Controler = "not yet"


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
    try:
        match key:
            case Keys.EXIT.value:
                MyMlx.loop_exit()
            case Keys.CELLS.value:
                Image.put_bg_affiche("affiche_ban.png", 0, 200)
                redrawing(0, Theme.color_bg, Theme.color_42, 0)
            case Keys.SWITCH_THEME.value:
                Theme.switch_theme()
                redrawing(0, Theme.color_bg, Theme.color_42, 0)
                redrawing(1, Theme.color_bg, Theme.color_42, 0)
            case Keys.SOLVE.value:
                path = generate_ouput_file(1)
                redrawing(2, Theme.color_bg, Theme.color_42, path)
            case Keys.MAZE.value:
                generate_ouput_file(0)
                redrawing(0, Theme.color_bg, Theme.color_42, 0)
                redrawing(1, Theme.color_bg, Theme.color_42, 0)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    Image.put_bg_affiche("maze_affiche.png", 0, 200)
    MyMlx.key_hook(call_back, None)
    MyMlx.loop()
