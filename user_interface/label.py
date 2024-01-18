import pygame

# Import internal module
from core.game_object import GameObject
from user_interface.font import Font, Text

class Label(GameObject):
    def __init__(self, x: int, y: int, text: str, color: tuple[int, int, int], font: Font, scale=1, centered=True) -> None:
        self.init_attributes()
        
        self._x = x
        self._y = y
        self.color = color
        self.font = font
        self.scale = scale
        self.centered = centered
        
        self._text = None
        self._textObj: Text = None
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if self._text == value:
            return
        self._text = value
        self._textObj = self.font.generateText(self._text, self.color, self.scale)

    def update(self):
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.font.renderText(self._x, self._y, self._textObj, surface, self.centered)
