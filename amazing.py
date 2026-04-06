from parser import Parser
from generater import MazeGenerator
from maze import Maze
from my_mlx import MyMlx

# from maze_controller import MazeController
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
        )

    # self.maze_controler = MazeController(self.maze_generator)

    def run(self):
        # self.maze_controler.start()
        # MyMlx.loop()
        self.generater.generate()


if __name__ == "__main__":
    amazing = Amazing()
    amazing.run()
    sys.exit(0)
