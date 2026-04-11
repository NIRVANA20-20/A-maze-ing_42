
from my_mlx.my_mlx import MyMlx
import os
from typing import Any


def create_color(r: int, g: int, b: int) -> int:
    col = 0xFF000000 | (r << 16) | (g << 8) | b
    return col


class Colors:
    BLACK = create_color(0, 0, 0)
    WHITE = create_color(255, 255, 255)

    ORANGE_MOOD_BG = create_color(255, 175, 102)
    ORANGE_MOOD_BR = create_color(153, 76, 0)
    ORANGE_MOOD_42 = create_color(12, 23, 34)

    PINK_MOOD_BG = create_color(255, 204, 255)
    PINK_MOOD_BR = create_color(153, 0, 76)
    PINK_MOOD_42 = create_color(82, 16, 82)

    BLUE_MOOD_BG = create_color(102, 255, 255)
    BLUE_MOOD_BR = create_color(10, 75, 75)
    BLUE_MOOD_42 = create_color(10, 75, 75)

    GRIS_MOOD_BG = create_color(224, 224, 224)
    GRIS_MOOD_BR = create_color(64, 64, 64)
    GRIS_MOOD_42 = create_color(84, 84, 80)


class Background:

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.abs_path = os.path.abspath(".") + "/Rendring/images/" + file_name
        self.img_ptr, _, _ = MyMlx.load_png_image(self.abs_path)

    def put_image_to_window(self) -> None:
        if self.img_ptr is not None:
            MyMlx.draw_image(self.img_ptr, 0, 0)


class Mood:

    def set_bg_color(self, bg_color: Any) -> Any:
        self.bg_color = bg_color
        return self

    def set_border_color(self, br_color: Any) -> Any:
        self.border_color = br_color
        return self

    def set_42_color(self, color_42: Any) -> Any:
        self.color_42 = color_42
        return self

    def set_background(self, file_name: str) -> Any:
        self.background = Background(file_name)
        return self


class Theme:

    START = Background("main_affiche.png")

    themes = [
        Mood()
        .set_background("orange_mood.png")
        .set_bg_color(Colors.ORANGE_MOOD_BG)
        .set_border_color(Colors.ORANGE_MOOD_BR)
        .set_42_color(Colors.ORANGE_MOOD_42),
        Mood()
        .set_background("pink_mood.png")
        .set_bg_color(Colors.PINK_MOOD_BG)
        .set_border_color(Colors.PINK_MOOD_BR)
        .set_42_color(Colors.PINK_MOOD_42),
        Mood()
        .set_background("gris_mood.png")
        .set_bg_color(Colors.GRIS_MOOD_BG)
        .set_border_color(Colors.GRIS_MOOD_BR)
        .set_42_color(Colors.GRIS_MOOD_42),
        Mood()
        .set_background("blue_mood.png")
        .set_bg_color(Colors.BLUE_MOOD_BG)
        .set_border_color(Colors.BLUE_MOOD_BR)
        .set_42_color(Colors.BLUE_MOOD_42),
    ]
    theme_index = 0
    current_mood = themes[theme_index]
    bg_img_ptr = current_mood.background
    bg_color = current_mood.bg_color
    border_color = current_mood.border_color
    color_42 = current_mood.color_42

    @classmethod
    def switch_theme(cls) -> Any:
        cls.theme_index = (cls.theme_index + 1) % len(cls.themes)
        current_mood = cls.themes[cls.theme_index]
        cls.bg_img_ptr = current_mood.background
        cls.bg_color = current_mood.bg_color
        cls.border_color = current_mood.border_color
        cls.color_42 = current_mood.color_42
