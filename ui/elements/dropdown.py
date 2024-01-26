from dataclasses import dataclass

import pygame

from ui.elements.button import Button
from ui.elements.label import Label
from ui.elements.labeled_sprite import LabeledSprite
from ui.elements.scroll import Scroll
from ui.game_object import GameObject


@dataclass
class DropDownInitData():
    """TODO
    """
    header: LabeledSprite | Label | Button
    body_rect: pygame.Rect
    scroll: Scroll
    option: GameObject

class DropDown(GameObject):
    """TODO
    """

    def __init__(self, x: int, y: int, data: DropDownInitData) -> None:
        super().__init__()
        self.drag_children = True

        self.contractible = isinstance(data.header, Button)
        self.x = x
        self.y = y
