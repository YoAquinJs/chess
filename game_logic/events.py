"""TODO"""

from typing import Callable

import pygame

type Callback[T] = Callable[[T], None]
type Pyevent = pygame.event.Event

class Event[T]:
    """TODO
    """

    def __init__(self) -> None:
        self._subscripted: set[Callback[T]] = set()

    def subscript(self, callback: Callback[T]) -> Callback[T]:
        """TODO
        """
        if callback in self._subscripted:
            raise ValueError(f"Already subscripted callback '{callback.__name__}'")
        self._subscripted.add(callback)
        return callback

    def unsubscript(self, callback: Callback[T]) -> None:
        """TODO
        """
        self._subscripted.remove(callback)

    def emit(self, arg: T) -> None:
        """TODO
        """
        for callback in self._subscripted:
            callback(arg)

class EventListener[T]:
    """TODO
    """

    def __init__(self, event: Event[T], callback: Callback[T]) -> None:
        self.event = event
        self.callback = callback
        event.subscript(self.callback)

    def __del__(self) -> None:
        self.event.unsubscript(self.callback)
