from pygame import Surface

from game_logic.game_object import GameObject
from ui.elements.label import Label
from ui.elements.sprite import Sprite

class LabeledSprite(Sprite):

    def __init__(self, x: int, y: int, label: Label, image: Surface, centered=False, pixelByPixel: bool = True, tint: tuple[int, int, int] = (255,255,255)):
        super().__init__(x, y, image, centered, pixelByPixel, tint)
        self.drag_children = True
        
        if label is None or label.text == "":
            raise ValueError("Label is not defined or empty")

        label.x = x
        label.y = y
        label.centered = True
        self.label = label
        self.add_child(0, label)

    @property
    def text(self) -> str:
        return self.label.text

    @text.setter
    def text(self, value: str):
        self.label.text = value
