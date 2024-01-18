import pygame

# Import internal module
from core.game_object import GameObject
from user_interface.font import Font, Text

class Label(GameObject):
    def __init__(self, x: int, y: int, text: Text, color: tuple[int, int, int], font: Font, centered=True) -> None:
        self.init_attributes()
        
        self._x = x
        self._y = y
        self.color = color
        self.font = font
        self.centered = centered
        
        self._text = text
        self.font.generateText(self._text, self.color)

    @property
    def text(self) -> str:
        return self._text.value

    @text.setter
    def text(self, value: str):
        if self._text.value == value:
            return
        self._text = Text(value, self._text.scale)
        self.font.generateText(self._text, self.color)

    @property
    def scale(self) -> float:
        return self._text.scale

    @scale.setter
    def scale(self, value: float):
        if self._text.scale == value:
            return
        self._text = Text(self._text.value, value)
        self.font.generateText(self._text, self.color)

    def update(self):
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.font.renderText(self._x, self._y, self._text, surface, self.centered)

    def __str__(self) -> str:
        return self._text.value
