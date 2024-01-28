"""This module contains the Serializable ABC,
which represents an object that can be serialized with the Serializer Class"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Serializable(ABC):
    """Serializable class interface
    """

    @abstractmethod
    def get_serialization_attrs(self) -> dict[str, Any]:
        """Gives a dictionary of the object's serialization attributes

        Returns:
            dict[str, Any]: Dictionary
        """

    @classmethod
    @abstractmethod
    def get_from_deserialize(cls, attrs: dict[str, Any], **kwargs: Any) -> Serializable:
        """Contructs the Object from the deserialized daa

        Args:
            attrs (dict[str, Any]): Deserialized data
            **kwargs (Any): Aditional arguments for the contructor

        Returns:
            Serializable: Contructed object
        """
