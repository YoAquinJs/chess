"""TODO"""

from typing import Callable

import pygame
from pygame.event import Event

from utils.errors import StaticClassInstanceError

Callback = Callable[[Event], None]
class EventHandler():
    """TODO
    """
    _events: dict[int, list[Callback]] = {
        pygame.QUIT : [],
        pygame.MOUSEBUTTONDOWN : [],
        pygame.MOUSEBUTTONUP : [],
    }

    @classmethod
    def subscript(cls, event: int, callback: Callback) -> None:
        """TODO
        """
        cls._events[event].append(callback)

    @classmethod
    def unsubscript(cls, event: int, callback: Callback) -> None:
        """TODO
        """
        cls._events[event].remove(callback)

    @classmethod
    def emit_events(cls) -> None:
        """TODO
        """
        for event in pygame.event.get():
            subscripted = cls._events.get(event.type)
            if subscripted is None:
                continue
            for subscript in subscripted:
                subscript(event)

    def __init__(self) -> None:
        raise StaticClassInstanceError(EventHandler)

class SceneEventRegister():
    """TODO
    """

    def __init__(self) -> None:
        pass
