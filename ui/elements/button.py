"""This module contains the button object, which is the UI element for button interactions"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import pygame

from ui.elements.label import Label
from ui.elements.sprite import Sprite
from ui.game_object import GameObject


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

    class State(Enum):
        """TODO
        """
        IDLE = auto()
        HOOVER = auto()
        PRESSED = auto()
        RELEASED = auto()

    def __init__(self, x: int, y: int, init_data: ButtonInitData) -> None:
        super().__init__()
        self.drag_children = True

        self._x = x
        self._y = y
        self.callback = init_data.callback

        self.sprite = init_data.sprite
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.add_child(0, self.sprite)

        if init_data.label is not None:
            init_data.label.x = self.x
            init_data.label.y = self.y
            self.add_child(1, init_data.label)

        self._state = self.State.IDLE

    @property
    def _state(self) -> Button.State:
        """TODO
        """
        return self.state

    @_state.setter
    def _state(self, value: Button.State) -> None:
        self.state = value

        shadow = 0
        if self.state == Button.State.IDLE:
            shadow = 0
        elif self.state == Button.State.HOOVER:
            shadow = 26
        elif self.state == Button.State.PRESSED:
            shadow = 33
        elif self.state == Button.State.RELEASED:
            shadow = 18
            self.callback()

        self.sprite.tint = (255-shadow,255-shadow,255-shadow)


    def update(self) -> None:
        """Update the button pressed status, and call the callback when pressed
        """
        on_hoover = self.sprite.rect.collidepoint(pygame.mouse.get_pos())
        on_pressed = pygame.mouse.get_pressed()[0]

        if self.state == Button.State.IDLE and on_hoover:
            self._state = Button.State.HOOVER
        elif self.state == Button.State.HOOVER:
            if not on_hoover:
                self._state = Button.State.IDLE
            elif on_pressed:
                self._state = Button.State.PRESSED
        elif self.state == Button.State.PRESSED:
            if not on_hoover:
                self._state = Button.State.IDLE
            elif not on_pressed:
                self._state = Button.State.RELEASED
        elif self.state == Button.State.RELEASED:
            if on_hoover:
                self._state = Button.State.PRESSED if on_pressed else Button.State.HOOVER
            else:
                self._state = Button.State.IDLE

    def render(self, surface: pygame.Surface):
        pass
