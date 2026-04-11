from my_mlx.mlx import Mlx
from typing import Any


class MyMlx:
    mlx = Mlx()
    screen_width: int = 1500
    screen_height: int = 2000
    mlx_ptr = mlx.mlx_init()
    _, screen_width_temp, screen_height = mlx.mlx_get_screen_size(mlx_ptr)
    win_ptr = mlx.mlx_new_window(
        mlx_ptr, screen_width, screen_height, "A-Maze-ing"
    )

    @classmethod
    def start_loop(cls) -> None:
        cls.mlx.mlx_loop(cls.mlx_ptr)

    @classmethod
    def set_loop_hook(cls, callback: Any, data: Any) -> None:
        cls.mlx.mlx_loop_hook(cls.mlx_ptr, callback, data)

    @classmethod
    def stop_loop(cls) -> None:
        cls.mlx.mlx_loop_exit(cls.mlx_ptr)

    @classmethod
    def set_key_handler(cls, callback: Any, data: Any) -> None:
        cls.mlx.mlx_key_hook(cls.win_ptr, callback, data)

    @classmethod
    def draw_image(cls, img_ptr: Any, x: int, y: int) -> None:
        cls.mlx.mlx_put_image_to_window(
            cls.mlx_ptr, cls.win_ptr, img_ptr, x, y)

    @classmethod
    def load_png_image(cls, filename: str) -> Any:
        return cls.mlx.mlx_png_file_to_image(cls.mlx_ptr, filename)

    @classmethod
    def create_image(cls, width: int, height: int) -> Any:
        return cls.mlx.mlx_new_image(cls.mlx_ptr, width, height)

    @classmethod
    def get_image_data(cls, img_ptr: Any) -> Any:
        return cls.mlx.mlx_get_data_addr(img_ptr)
