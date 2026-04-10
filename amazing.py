from Parsing.parser import Parser
from Mazegen.generater import MazeGenerator, DfsGenerator
from Mazegen.maze import Maze
from my_mlx.my_mlx import MyMlx
from A_maze_ing.maze_controller import MazeController
import sys


class Amazing:
    def __init__(self):
        self.parser = Parser()

        self.generater = MazeGenerator(
            self.parser.width,
            self.parser.height,
            self.parser.entry,
            self.parser.exit,
            self.parser.seed,
            self.parser.perfect,
            self.parser.file_name,
        )
        self.maze = Maze()
        (
            self.maze.set_dimension(self.generater.width, self.generater.height)
            .set_exit(self.generater.exit)
            .set_entry(self.generater.entry)
            .set_file_name(self.generater.file_name)
            .set_perfect(self.generater.perfect)
            .set_seed(self.generater.seed)
            .set_path(self.generater.path)
            .set_grid(self.generater.grid)
        )

        self.maze_controler = MazeController(self.generater)

    def run(self):
        self.maze_controler.start()
        MyMlx.loop()
    


if __name__ == "__main__":
    try:
        amazing = Amazing()
        amazing.run()
        sys.exit(0)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
