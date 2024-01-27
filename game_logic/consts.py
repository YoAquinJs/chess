"""This module contains constants for all subsystems of the app"""

#! This module shouldn't import from any other app module
from __future__ import annotations

from enum import Enum
from os import getcwd, makedirs, path

# Rendering Constants
SCREEN_SIZE = 4

# Serialization constants
MAX_GAMES_SAVED = 5

class AssetType(Enum):
    """Enum for assets types containing corresponding paths
    """
    SPRITE=path.join(getcwd(),"assets","sprites")
    AUDIO=path.join(getcwd(),"assets","audios")
    SAVINGS=path.join(getcwd(),"savings")

if not path.exists(AssetType.SAVINGS.value):
    makedirs(AssetType.SAVINGS.value)

class PrintColor(Enum):
    """Enum for console print colors
    """
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[96m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'
