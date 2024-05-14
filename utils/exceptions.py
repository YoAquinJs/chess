"""TODO"""


class EnumParseError(Exception):
    """Raise when the enum parse fails"""

class InvalidChessGameError(Exception):
    """Raise when a chess game it's initialized with invalid data"""

class InvalidGridError(Exception):
    """Raise when a chess game it's initialized with invalid data"""

class GridIndexError(Exception):
    """Raise when accesing invalid grid positions"""

class StaticClassInstanceError(Exception):
    """Raise when trying to instance a static class"""
    def __init__(self, callee_class: type):
        message = f"{callee_class.__name__} is a static class, thus cannot be instanced"
        super().__init__(message)
