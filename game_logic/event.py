"""TODO"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Event[T]():
    """TODO
    """

    mapped_int: int
    _callbacks: list[Callable[[T], None]] = []

    def subscript(self, callback: Callable[[T], None]) -> None:
        """TODO
        """
        self._callbacks.append(callback)

    def unsubscript(self, callback: Callable[[T], None]) -> None:
        """TODO
        """
        self._callbacks.remove(callback)

    def clear(self) -> None:
        """TODO
        """
        self._callbacks.clear()

    def emit(self, value: T) -> None:
        """TODO
        """
        for callback in self._callbacks:
            callback(value)
