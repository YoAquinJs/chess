"""This module contains the button object, which is the UI element for button interactions"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional

import pygame

from ui.game_object import GameObject
from ui.elements.label import Label
from ui.elements.sprite import Sprite


@dataclass
class ButtonInitData():
    """TODO
    """
    sprite: Sprite
    label: Optional[Label]
    callback: Callable[[], None]

class Button(GameObject):
    """TODO
    """
    def __init__(self, x: int, y: int, init_data: ButtonInitData) -> None:
        super().__init__()
        self.drag_children = True

        self._x = x
        self._y = y
        self.pressed = False
        self.callback = init_data.callback

        self.sprite = init_data.sprite
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.add_child(0, self.sprite)

        if init_data.label is not None:
            init_data.label.x = self.x
            init_data.label.y = self.y
            self.add_child(1, init_data.label)

    def update(self) -> None:
        """Update the button pressed status, and call the callback when pressed
        """
        def overshadow(tint: tuple[int, int, int], increase: int):
            return (tint[0]-increase,tint[1]-increase,tint[2]-increase)

        mouse_over_btt = self.sprite.rect.collidepoint(pygame.mouse.get_pos())
        left_mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.pressed: # On realease
            if not mouse_over_btt:
                self.pressed = False
            elif not left_mouse_pressed:
                self.pressed = False
                self.callback()

        tint = (255,255,255)
        if mouse_over_btt:
            tint = overshadow(tint, 25)
            if left_mouse_pressed:
                tint = overshadow(tint, 30)
                self.pressed = True

        self.sprite.tint = tint

    def render(self, surface: pygame.Surface):
        pass
