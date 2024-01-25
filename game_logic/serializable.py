"""TODO"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Serializable(ABC):
    """Serializable class interface
    """

    @abstractmethod
    def get_serialization_attrs(self) -> dict[str, Any]:
        """TODO
        """

    @abstractmethod
    @classmethod
    def get_from_deserialize(cls, attrs: dict[str, Any]) -> Serializable:
        """TODO
        """
