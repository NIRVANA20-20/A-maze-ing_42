from typing import Any


class Maze:

    _instance = None
    _is_init = 0
    entry: tuple[int, int]
    exit: tuple[int, int]

    def __new__(cls) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_dimension(self, width: int, height: int) -> Any:
        self.width = width
        self.height = height
        return self

    def set_grid(self, grid: Any) -> Any:
        self.grid = grid
        return self

    def set_entry(self, m_entry: Any) -> "Maze":
        self.entry: int = m_entry
        return self

    def set_exit(self, m_exit: Any) -> "Maze":
        self.exit = m_exit
        return self

    def entry_exit_maze(self, entry: Any, exit: Any) -> Any:
        self.entry = entry
        self.exit = exit
        return self

    def set_width(self, width: int) -> Any:
        self.width = width
        return self

    def set_file_name(self, file_name: str) -> Any:
        self.file_name = file_name
        return self

    def set_perfect(self, perfect: bool) -> Any:
        self.perfect = perfect
        return self

    def set_seed(self, seed: int) -> Any:
        self.seed = seed
        return self

    def set_path(self, path: Any) -> Any:
        self.path = path
        return self
