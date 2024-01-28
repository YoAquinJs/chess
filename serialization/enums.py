"""TODO"""

from enum import Enum, auto


class SerializeStatus(Enum):
    """Result status for serialization
    """
    SUCCESFULL = auto()
    MAX_SAVES_REACHED = auto()
    NOT_FOUND = auto()
    INCORRECT_OBJ_TYPE=auto()

class DeserializeStatus(Enum):
    """Result status for deserialization
    """
    SUCCESFULL = auto()
    NOT_FOUND = auto()
    MISSING_ATTRS = auto()
