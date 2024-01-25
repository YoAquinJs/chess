import pygame

from typing import Union
from game_logic.game_object import GameObject
from ui.elements.button import Button
from ui.elements.label import Label
from ui.elements.labeled_sprite import LabeledSprite
from ui.elements.scroll import Scroll

class DropDown(GameObject):
    
    def __init__(self, x: int, y: int, header: Union[LabeledSprite, Label, Button], bodyRect: pygame.Rect, scroll: Scroll, option: GameObject) -> None:
        super().__init__()
        
        self.contractible = isinstance(header, Button)
        self.x = x
        self.y = y

    @GameObject.x.setter
    def x(self, value):
        delta = value - self._x
        super().x.__set__(self, value)
        for child in self.children:
            child.x += delta

    @GameObject.y.setter
    def y(self, value):
        delta = value - self._y
        super().y.__set__(self, value)
        for child in self.children:
            child.y += delta