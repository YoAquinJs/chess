"""TODO"""

from dataclasses import dataclass

import pygame

# Import internal module
from ui.game_object import GameObject
from ui.font import Font, Text


@dataclass
class LabelInitData():
    """TODO
    """
    text: Text
    color: tuple[int, int, int]
    font: Font
    centered=True

class Label(GameObject):
    """TODO
    """

    def __init__(self, x: int, y: int, init_data: LabelInitData) -> None:
        super().__init__()

        self._x = x
        self._y = y
        self.color = init_data.color
        self.font = init_data.font
        self.centered = init_data.centered

        self._text = init_data.text
        self.font.generate_text(self._text, self.color)

    @property
    def text(self) -> str:
        """Text property
        """
        return self._text.value

    @text.setter
    def text(self, value: str) -> None:
        if self._text.value == value:
            return
        self._text = Text(value, self._text.scale)
        self.font.generate_text(self._text, self.color)

    @property
    def scale(self) -> float:
        """Scale property
        """
        return self._text.scale

    @scale.setter
    def scale(self, value: float) -> None:
        if self._text.scale == value:
            return
        self._text = Text(self._text.value, value)
        self.font.generate_text(self._text, self.color)

    def update(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        rx, ty = self.x, self.y
        if self.centered:
            rx, ty = self.font.center_text_coords(rx, ty, self._text)
        self.font.render_text(rx, ty, self._text, surface)

    def __str__(self) -> str:
        return self._text.value
