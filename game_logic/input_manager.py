"""TODO"""

from utils.exceptions import StaticClassInstanceError


class InputManager():
    def __init__(self) -> None:
        raise StaticClassInstanceError(InputManager)
