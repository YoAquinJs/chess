"""This module contains constants for all subsystems of the app"""

#! This module shouldn't import from any other app module
from os import getcwd, makedirs, path
from enum import Enum, EnumMeta

# Paths
SPRITE = 'assets/sprites/'
AUDIO = 'assets/audios/'
SAVINGS = f"{getcwd()}/savings/"

if not path.exists(SAVINGS):
    makedirs(SAVINGS)
    
class PrintColor(Enum):
    """Enum for console print colors"""
    
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    reset = '\033[0m'
    
# Meta Enum class for parsing from string value to Enum
class ParseableEnum(EnumMeta):
    def __getitem__(cls, item: str) -> object:
        """This method parse from a string to the Enum object

        Args:
            item (str): The string to be parsed

        Returns:
            object: This enum
        """
        
        match = None
        for member in cls.__members__.values():
            if member.value == item:
                match = member
                break
        
        if match is None:
            raise KeyError(f"No such value in {cls.__name__}: {item}")
        
        return match
    
class TestType(Enum, metaclass=ParseableEnum):
    """Enum for the multiple test type"""

    board = 'board'
    piece = 'piece'
    game = 'game'

# Unique identifiers for players, always a single character
class PlayerColor(Enum, metaclass=ParseableEnum):
    """Enum for piece color"""

    white = 'w'
    black = 'b'
    empty = '#'

# Unique identifiers for game states
class GameResult(Enum):
    """Enum for endding states in a chess game"""

    pending = 'pending'
    whiteWin = 'whiteWin'
    blackWin = 'blackWin'
    stalemate = 'stalemate'
    tie = 'tie'

class BoardState(Enum):
    """Enum for states in a chess game"""

    moveTurn = 'moveTurn'
    check = 'check'
    checkmate = 'checkmate'
    stalemate = 'stalemate'

class GameScreen(Enum):
    """Enum for states in a chess game"""

    mainMenu = 'move_turn'
    settings = 'settings'
    onGame = 'on_game'

# Unique identifiers for pieces, always a single character, the format it's f"{PlayerColor}{PieceType}"
class PieceType(Enum, metaclass=ParseableEnum):
    """Enum for each type of piece"""

    pawn = 'P'
    bishop = 'B'
    knigth = 'K'
    rook = 'R'
    queen = 'Q'
    king = '@'
    empty = '#'
    
# It's assumed you can never move to a square with a piece of your own
class MovementSpecialCase(Enum):
    """Enum for each type of piece"""

    castle = 'canCastle'
    isEmpty = 'isEmpty'
    doublePawnMove = 'doublePawnMove'
    
# Constants for board
ROWS    = ['8','7','6','5','4','3','2','1']
COLUMNS = ['a','b','c','d','e','f','g','h']
BLACK_MOV_DIR = 1
WHITE_MOV_DIR = -1

BOARD_START = [
    ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'], # 8
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'], # 7
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 6
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 5
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 4
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 3
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'], # 2
    ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']  # 1
#     a     b     c     d      e     f     g     h
]
# The start board has type List[List[str]], when used, the board class converts it to List[List[Piece]]