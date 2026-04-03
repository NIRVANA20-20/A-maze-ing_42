from parser import Parser
from generater import Maze, MazeGenerator, MazeSolver
from my_mlx import MyMlx
from enum import Enum
from rendrer import Image, DrawAnimation, MazeCreator, Theme


class Keys(Enum):
    EXIT = 65507
    CELLS = 65293
    SWITCH_THEME = 99
    SOLVE = 112
    MAZE = 32


class StepsControler:
    step_con = None


def redrawing(flag, color_bg, color_42, path):

    file_parsed = Parser()
    file_parsed.read_config()
    width, height, entry, exit, _, _ = file_parsed.get_infos()
    maze = Maze()
    maze.maze_attribute(width, height, entry, exit)
    cell_dim, _, _ = MazeCreator.get_dim_pos(maze)
    border = MazeCreator(maze, cell_dim)
    drawer = DrawAnimation(path, color_bg)

    if flag == 0:
        border.creat_cells(color_42, color_bg)
    if flag == 1:
        drawer.draw_dfs()
        StepsControler.step_con = Keys.MAZE
    if flag == 2:
        path_list = []
        for i in range(len(path) - 1):
            destination = DrawAnimation.path_checker(path[i], path[i + 1])
            path_list.append(destination)
        drawer.draw_entry_exit(entry, exit)
        drawer.draw()


def generate_ouput_file(flage: int) -> list:
    file_parsed = Parser()
    _, _, entry, exit, _, _ = file_parsed.get_infos()
    maze = Maze()
    generator = MazeGenerator(maze)

    if flage == 0:
        maze.grid_maze()
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
                if Parser.controler() == 1 and StepsControler.step_con is None:
                    Theme.switch_theme()
                    Image.put_bg_affiche(Theme.bg_img, 0, 0)
                    redrawing(0, Theme.color_bg, Theme.color_42, 0)
                    StepsControler.step_con = Keys.CELLS
                else:
                    MyMlx.loop_exit()

            case Keys.SWITCH_THEME.value:
                Theme.switch_theme()
                Image.put_bg_affiche(Theme.bg_img, 0, 0)
                redrawing(0, Theme.color_bg, Theme.color_42, 0)
                redrawing(1, Theme.color_bg, Theme.color_42, 0)

            case Keys.SOLVE.value:
                if StepsControler.step_con == Keys.SOLVE:
                    print(StepsControler.step_con)
                    path = generate_ouput_file(1)
                    redrawing(2, Theme.color_bg, Theme.color_42, path)
                    StepsControler.step_con = None

            case Keys.MAZE.value:
                if (
                    StepsControler.step_con == Keys.CELLS
                    or StepsControler.step_con == Keys.MAZE
                ):
                    generate_ouput_file(0)
                    Image.put_bg_affiche(Theme.bg_img, 0, 0)
                    redrawing(0, Theme.color_bg, Theme.color_42, 0)
                    redrawing(1, Theme.color_bg, Theme.color_42, 0)
    except Exception as e:
        print(e)
        Keys.EXIT
    finally:
        if StepsControler.step_con == Keys.MAZE:
            StepsControler.step_con = Keys.SOLVE


class AmazeIng:
    class __init__(self):
        pass


if __name__ == "__main__":

    Image.put_bg_affiche("main_affiche.png", 0, 0)
    MyMlx.key_hook(call_back, None)
    MyMlx.loop()
