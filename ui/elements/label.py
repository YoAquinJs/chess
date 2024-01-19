import pygame

# Import internal module
from game_logic.game_object import GameObject
from ui.font import Font, Text

class Label(GameObject):
    def __init__(self, x: int, y: int, text: Text, color: tuple[int, int, int], font: Font, centered=True) -> None:
        self.init_attributes()
        
        self._x = x
        self._y = y
        self.color = color
        self.font = font
        self.centered = centered
        
        self._text = text
        self.font.generate_text(self._text, self.color)

    @property
    def text(self) -> str:
        return self._text.value

    @text.setter
    def text(self, value: str) -> None:
        if self._text.value == value:
            return
        self._text = Text(value, self._text.scale)
        self.font.generate_text(self._text, self.color)

    @property
    def scale(self) -> float:
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
        self.font.render_text(self._x, self._y, self._text, surface, self.centered)

    def __str__(self) -> str:
        return self._text.value
