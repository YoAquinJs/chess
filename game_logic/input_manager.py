"""TODO"""

from enum import IntEnum, auto
from typing import Any

import pygame

from game_logic.events import Callback, Event, EventListener, Pyevent
from utils.errors import StaticClassInstanceError


class InputType(IntEnum):
    """TODO
    """
    R_MOUSE_DOWN = auto()
    R_MOUSE_UP = auto()
    L_MOUSE_DOWN = auto()
    L_MOUSE_UP = auto()

class InputManager():
    """TODO
    """

    _events: dict[InputType, Event[Any]] = {
        InputType.R_MOUSE_DOWN : Event[tuple[int, int]](),
        InputType.R_MOUSE_UP : Event[tuple[int, int]](),
        InputType.L_MOUSE_DOWN : Event[tuple[int, int]](),
        InputType.L_MOUSE_UP : Event[tuple[int, int]](),
    }

    @classmethod
    def mouse_down_map(cls, pyevent: Pyevent):
        """TODO
        """
        mouse_pos = pygame.mouse.get_pos()
        if pyevent.button == 1:
            cls._events[InputType.L_MOUSE_DOWN].emit(mouse_pos)
        if pyevent.button == 3:
            cls._events[InputType.L_MOUSE_DOWN].emit(mouse_pos)

    @classmethod
    def mouse_up_map(cls, pyevent: Pyevent):
        """TODO
        """
        mouse_pos = pygame.mouse.get_pos()
        if pyevent.button == 1:
            cls._events[InputType.L_MOUSE_UP].emit(mouse_pos)
        if pyevent.button == 3:
            cls._events[InputType.L_MOUSE_UP].emit(mouse_pos)

    @classmethod
    def get(cls, inpt: InputType, callback: Callback[Any]) -> EventListener[Any]:
        """TODO
        """
        return EventListener(cls._events[inpt], callback)


    def __init__(self) -> None:
        raise StaticClassInstanceError(InputManager)
