"""TODO"""

from enum import Enum
from typing import cast

import chess_engine.enums as chess_engine_enums
from utils.parseable_enum import ParseableEnum

parseable_enums = chess_engine_enums

def test_parseable_enums() -> None:
    """TODO
    """
    for enum in parseable_enums.__dict__.values():
        if not isinstance(enum, ParseableEnum):
            continue

        for value in enum:
            assert value == enum[cast(Enum, value).value]
