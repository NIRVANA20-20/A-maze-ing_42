from my_mlx.my_mlx import MyMlx
from typing import Any
from Themes.themes import Theme


class Image:
    _instance = None
    _is_init = 0

    def __new__(cls) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_dimension(self, width: Any, height: Any) -> Any:
        min_screen = min(MyMlx.screen_height, MyMlx.screen_width)
        max_cell = max(width, height)
        self.cell_dim = int((min_screen / max_cell) * 0.75)
        self.cell_b = int(self.cell_dim * 0.10)
        self.height = int(height * self.cell_dim + self.cell_b)
        self.width = int(width * self.cell_dim + self.cell_b)
        self.poss_w = int((MyMlx.screen_width - width * self.cell_dim) / 2)
        self.poss_h = 200
        return self

    def img_ptr(self) -> Any:
        self.ptr = MyMlx.create_image(self.width, self.height)
        return self

    def img_data_addr(self) -> Any:
        self.buffer, self.bpp, self.sl, self.format = MyMlx.get_image_data(
            self.ptr
        )
        return self

    def put_pixel(self, x: int, y: int, color: int) -> None:
        offset = int((y * self.sl) + (x * (self.bpp // 8)))
        self.buffer[offset: offset + 4] = color.to_bytes(4, "little")

    def put_north(self, x: Any, y: Any, color: Any, cell_br: int = 0) -> None:
        start_h = y * self.cell_dim
        start_w = x * self.cell_dim
        cell_width = self.cell_dim * (x + 1)
        for y in range(start_h, self.cell_b + start_h):
            for x in range(
                start_w + cell_br, cell_width + self.cell_b - cell_br
            ):
                self.put_pixel(x, y, color)

    def put_west(self, x: Any, y: Any, color: Any, cell_br: int = 0) -> None:
        start_h = y * self.cell_dim
        start_w = x * self.cell_dim
        cell_height = self.cell_dim * (y + 1)
        for x in range(start_w, start_w + self.cell_b):
            for y in range(
                start_h + cell_br, cell_height + self.cell_b - cell_br
            ):
                self.put_pixel(x, y, color)

    def put_south(self, x: Any, y: Any, color: Any, cell_br: int = 0) -> None:
        start_h = y * self.cell_dim
        start_w = self.cell_dim * x
        cell_width = self.cell_dim * (x + 1)
        for x in range(start_w + cell_br, cell_width + self.cell_b - cell_br):
            for y in range(
                start_h + self.cell_dim, self.cell_b + self.cell_dim + start_h
            ):
                self.put_pixel(x, y, color)

    def put_east(self, x: Any, y: Any, color: Any, cell_br: int = 0) -> None:
        start_h = y * self.cell_dim
        start_w = self.cell_dim * (x + 1)
        cell_height = self.cell_dim * (y + 1)
        for x in range(start_w, start_w + self.cell_b):
            for y in range(
                start_h + cell_br, cell_height + self.cell_b - cell_br
            ):
                self.put_pixel(x, y, color)

    def put_img(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.put_pixel(x, y, Theme.bg_color)

    def put_inside(self, x: Any, y: Any) -> None:
        start_h = y * self.cell_dim + self.cell_b
        start_w = x * self.cell_dim + self.cell_b
        cell_width = self.cell_dim * (x + 1)
        for y in range(start_h, self.cell_dim + start_h):
            for x in range(start_w, cell_width + self.cell_b):
                self.put_pixel(x, y, Theme.color_42)

    def put_entry_exit(self, x: Any, y: Any) -> None:
        start_h = y * self.cell_dim + (2 * self.cell_b)
        start_w = x * self.cell_dim + (2 * self.cell_b)
        cell_width = self.cell_dim * (x + 1)
        for y in range(start_h, self.cell_dim + start_h - (3 * self.cell_b)):
            for x in range(
                start_w, cell_width + self.cell_b - (2 * self.cell_b)
            ):
                self.put_pixel(x, y, Theme.color_42)

    def put_path(self, x: Any, y: Any, destination: Any) -> None:
        start_h = y * self.cell_dim + (self.cell_dim // 3)
        start_w = x * self.cell_dim + (self.cell_dim // 3)

        if destination == "N":
            for y in range(start_h - self.cell_dim, start_h):
                for x in range(start_w, start_w + (self.cell_dim // 3)):
                    self.put_pixel(x, y, Theme.color_42)

        elif destination == "S":
            for y in range(
                start_h, self.cell_dim + (self.cell_dim // 3) + start_h
            ):
                for x in range(start_w, start_w + (self.cell_dim // 3)):
                    self.put_pixel(x, y, Theme.color_42)

        elif destination == "E":
            for y in range(start_h, start_h + self.cell_dim // 3):
                for x in range(
                    start_w, start_w + self.cell_dim + self.cell_dim // 3
                ):
                    self.put_pixel(x, y, Theme.color_42)

        elif destination == "W":
            for y in range(start_h, start_h + self.cell_dim // 3):
                for x in range(start_w - self.cell_dim, start_w):
                    self.put_pixel(x, y, Theme.color_42)
