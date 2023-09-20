from enum import Enum, EnumMeta

# Paths to asset folders
SPRITE = 'assets/sprites/'
AUDIO = 'assets/audios/'

# Meta Enum class for parsing from string value to Enum
class CustomEnumMeta(EnumMeta):
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

# Unique identifiers for players, always a single character
class PlayerColor(Enum, metaclass=CustomEnumMeta):
    """Enum for piece color"""

    white = 'w'
    black = 'b'

# Unique identifiers for game states
class OnGameState(Enum):
    """Enum for states in a chess game"""

    move_turn = 'move_turn'
    check = 'check'
    checkmate = 'checkmate'
    stalemate = 'stalemate'
    tie = 'tie'

class GameScreen(Enum):
    """Enum for states in a chess game"""

    main_menu = 'move_turn'
    settings = 'settings'
    on_game = 'on_game'

# Unique identifiers for pieces, always a single character, the format it's f"{PieceType}{PlayerColor}"
class PieceType(Enum, metaclass=CustomEnumMeta):
    """Enum for each type of piece"""

    pawn = 'P'
    bishop = 'B'
    knigth = 'K'
    rook = 'R'
    queen = 'Q'
    king = '@'
    empty = '#'
    
# Constants for board
COLUMNS = ['a','b','c','d','e','f','g','h']
ROWS    = ['8','7','6','5','4','3','2','1']

"""
8 bR bK bB bQ b@ bB bK bR
7 bP bP bP bP bP bP bP bP
6 ## ## ## ## ## ## ## ##
5 ## ## ## ## ## ## ## ##
4 ## ## ## ## ## ## ## ## 
3 ## ## ## ## ## ## ## ##
2 wP wP wP wP wP wP wP wP
1 wR wK wB wQ w@ wB wK wR
  a  b  c  d  e  f  g  h
"""
back_rank = [PieceType.rook.value,PieceType.knigth.value,PieceType.bishop.value,PieceType.queen.value,
             PieceType.king.value,PieceType.bishop.value,PieceType.knigth.value,PieceType.rook.value]
pawn_rank = [PieceType.pawn.value,PieceType.pawn.value,PieceType.pawn.value,PieceType.pawn.value,
             PieceType.pawn.value,PieceType.pawn.value,PieceType.pawn.value,PieceType.pawn.value]
empty_rank = [PieceType.empty.value,PieceType.empty.value,PieceType.empty.value,PieceType.empty.value,
              PieceType.empty.value,PieceType.empty.value,PieceType.empty.value,PieceType.empty.value]
BOARD_START = {row: {key: value for key, value in zip(COLUMNS, empty_rank)} for row in ROWS}
BOARD_START['8'] = {key: value for key, value in zip(COLUMNS, [x+PlayerColor.black.value for x in back_rank])}
BOARD_START['7'] = {key: value for key, value in zip(COLUMNS, [x+PlayerColor.black.value for x in pawn_rank])}
BOARD_START['2'] = {key: value for key, value in zip(COLUMNS, [x+PlayerColor.white.value for x in pawn_rank])}
BOARD_START['1'] = {key: value for key, value in zip(COLUMNS, [x+PlayerColor.white.value for x in back_rank])}
# The start board has type Dict[str, Dict[str, str]], when used, the board class converts it to Dict[str, Dict[str, Piece]]