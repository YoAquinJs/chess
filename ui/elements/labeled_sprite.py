from pygame import Surface

from game_logic.game_object import GameObject
from ui.elements.label import Label
from ui.elements.sprite import Sprite

class LabeledSprite(Sprite):

    def __init__(self, x: int, y: int, label: Label, image: Surface, centered=False, pixelByPixel: bool = True, tint: tuple[int, int, int] = (255,255,255)):
        super().__init__(x, y, image, centered, pixelByPixel, tint)
        
        if label is None or label.value == "":
            raise ValueError("Label is not defined or empty")
        
        label.x = x
        label.y = y
        self.label = label
        self.add_child(0, label)

    @GameObject.x.setter
    def x(self, value):
        delta = value - self._x
        for child in self.children:
            child.x += delta
        super().xSetter(value)

    @GameObject.y.setter
    def y(self, value):
        delta = value - self._y
        for child in self.children:
            child.y += delta
        super().ySetter(value)