"""TODO"""

from typing import Callable

type Callback[T] = Callable[[T], None]

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
