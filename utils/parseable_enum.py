"""TODO"""

from __future__ import annotations

from enum import EnumMeta
from typing import cast

from utils.exceptions import EnumParseError


class ParseableEnum(EnumMeta):
    """Makes a string parseable to the specified enum type
    """
    def __getitem__(cls, item: str) -> ParseableEnum:
        """This method parse from a string to the Enum object

        Args:
            item (str): The string to be parsed

        Returns:
            ParseableEnum: This enum
        """
        if item not in cls.__members__.keys():
            raise EnumParseError(f"No such value in {cls.__name__}: {item}")

        found = cls.__members__.get(item)
        return cast(ParseableEnum, found)
