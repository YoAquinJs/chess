"""This module contains the button object, which is the UI element for button interactions"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import pygame

from game_logic.game_object import GameObject
from game_logic.input_manager import InputManager, InputType
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

    class State(Enum):
        """TODO
        """
        IDLE = auto()
        HOOVER = auto()
        PRESSED = auto()

    def __init__(self, x: int, y: int, init_data: ButtonInitData) -> None:
        GameObject.__init__(self)
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

        self._hover = False
        self._state = self.State.IDLE
        self._on_press_event = InputManager.get(InputType.L_MOUSE_DOWN, self._on_press)
        self._on_release_event = InputManager.get(InputType.L_MOUSE_UP, self._on_release)

    @property
    def state(self) -> Button.State:
        """TODO
        """
        return self._state

    @state.setter
    def state(self, value: Button.State) -> None:
        self._state = value

        shadow = 0
        if self._state == Button.State.HOOVER:
            shadow = 15
        elif self._state == Button.State.PRESSED:
            shadow = 30

        self.sprite.tint = (255-shadow,255-shadow,255-shadow)

    def update(self) -> None:
        """Update the button pressed status, and call the callback when pressed
        """
        self._hover = self.sprite.rect.collidepoint(pygame.mouse.get_pos())
        if not self._hover:
            self.state = Button.State.IDLE
        elif self._state == Button.State.IDLE:
            self.state = Button.State.HOOVER

    def _on_press(self, mouse_pos: tuple[int, int]) -> None:
        if self._hover:
            self.state = Button.State.PRESSED
            print("button press", mouse_pos)

    def _on_release(self, mouse_pos: tuple[int, int]) -> None:
        if self._state == Button.State.PRESSED:
            self.state = Button.State.HOOVER
            self.callback()
            print("button release", mouse_pos)

    def render(self, surface: pygame.Surface):
        pass
