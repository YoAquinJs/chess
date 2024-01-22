"""TODO"""

from ui.elements.label import Label
from ui.elements.sprite import Sprite, SpriteInitData


class LabeledSprite(Sprite):
    """TODO
    """

    def __init__(self, x: int, y: int, label: Label, init_data: SpriteInitData):
        super().__init__(x, y, init_data)
        self.drag_children = True

        if label.text == "":
            raise ValueError("Label is empty")

        label.x = x
        label.y = y
        label.centered = True
        self.label = label
        self.add_child(0, label)

    @property
    def text(self) -> str:
        """Text property
        """
        return self.label.text

    @text.setter
    def text(self, value: str):
        self.label.text = value
