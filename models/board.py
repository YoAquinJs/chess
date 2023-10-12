"""This module contains the Board model object and it's properties"""

import sys
from json import dumps, load
from typing import Dict, Union, List

from models.consts import PieceType, PlayerColor, MovementSpecialCase, COLUMNS, ROWS, BOARD_START, SAVINGS
from models.piece import Piece

class Board():
    """Class for handling game screens, and game states

    Attributes:
        __grid (List[List[Piece]]): Grid representing the board configuration, it's private
        canCastle (bool): Whether castling is available for this board or not. Defaults to True.
        check (bool): Whether the player whoose turn is next is checked or not. Defaults to False.
        possibleEnPassant (Union[int, int]]): Coordinates of a possible en passant movement for the next turn.
        whitePieces (List[Piece]): List of all pieces of color white.
        blackPieces (List[Piece]): List of all pieces of color black.
        #//attackedSquares (Union[int, int]]): List of the positions attacked by the opponent pieces in this turn
        turn (PlayerColor): The player whoose turn it's the on going one. Defaults to PlayerColor.white.
    """

    def __init__(self, grid: List[List[Piece]]) -> None:
        """Creates a board object instance

        Args:
            __grid (List[List[Piece]]): Grid representing the chess board and the game pieces.
        """
        
        self.__grid = grid
        
        # Default board params
        self.canCastle = False
        self.check = False
        self.turn = PlayerColor.white
        self.possibleEnPassant = None
        
        # Get all the color pieces in their correspondent lists
        self.whitePieces = []
        self.blackPieces = []
        
        for row in range(len(ROWS)):
            for column in range(len(COLUMNS)):
                piece = self.__grid[row][column]
                if piece.type != PieceType.empty:
                    self.whitePieces.append(piece) if piece.color == PlayerColor.white else self.blackPieces.append(piece)
                    
        self.attackedSquares = []
        self.squares_under_attack()

    def select_square(self, row: int, column: int) -> Piece:
        """Returns the piece in the specified square

        Args:
            row (int): Specified row
            column (int): Specified column

        Returns:
            Piece: Piece in the square
        """
        
        return self.__grid[row][column]

    def is_empty(self, row: int, column: int) -> bool:
        """Returns whether the square is empty or not

        Args:
            row (int): Row
            column (int): Column

        Returns:
            bool: Empty or not
        """
        
        return self.__grid[row][column].type == PieceType.empty

    def is_opponent(self, row: int, column: int, playerColor: PlayerColor) -> bool:
        """Returns whether the square is ocuppied by an opponent piece or not

        Args:
            row (int): Row
            column (int): Column
            playerColor(PlayerColor): The player which is checking for the opponent color

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].type != PieceType.empty and self.__grid[row][column].color != playerColor

    def is_player(self, row: int, column: int, playerColor: PlayerColor) -> bool:
        """Returns whether the square is ocuppied by a piece of the player or not

        Args:
            row (int): Row
            column (int): Column
            playerColor(PlayerColor): The player which is checking for it's color

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].type != PieceType.empty and self.__grid[row][column].color == playerColor

    def squares_under_attack(self):
        """Calculate the squares under attack by the opponent pieces
        """
        
        self.check = False
        self.attackedSquares = []
        
        turnPieces = self.blackPieces if self.turn == PlayerColor.black else self.whitePieces
        opponentPieces = self.whitePieces if self.turn == PlayerColor.black else self.blackPieces
        opponentKing = [item for item in opponentPieces if item.type == PieceType.king][0]
        
        # iterate trougth all the opponent pieces, and determine if anyone can move to the desired square
        for turnPiece in turnPieces:
            for movement in self.get_valid_movements(turnPiece, True):
                if movement not in self.attackedSquares:
                    self.attackedSquares.append(movement)
                if movement[0] == opponentKing.row and movement[1] == opponentKing.column:
                    self.check = True

    def swap_pieces(self, row1: int, column1: int, row2: int, column2: int):
        """Swap the piece from the square 1, with the piece with the square 2

        Args:
            row1 (int): Row for square 1
            column1 (int): column for square 1
            row2 (int): Row for square 2
            column2 (int): column for square 2
        """
        
        self.__grid[row1][column1].row = row2
        self.__grid[row1][column1].column = column2
        self.__grid[row2][column2].row = row1
        self.__grid[row2][column2].column = column1
        self.__grid[row1][column1], self.__grid[row2][column2] = self.__grid[row2][column2], self.__grid[row1][column1]

    def get_max_extendable_movements(self, piece: Piece, direction: Union[int, int], limitRow: int, limitColumn: int, includePossibleChecks: bool) -> int:
        """Given a piece and direction, returns the number of movements it can perform before reaching a given limit

        Args:
            piece (Piece): Piece to move.
            direction (Union[int, int]): Direction of the extenable movement.
            limitRow (int): The limit row that the extendable movement can go to.
            limitColumn (int): The limit column that the extendable movement can go to.
            includePossibleChecks (bool): Determine whether it should include movements to pieces of itself
            
        Returns:
           Int: Maximun number of movements in that direction.
        """
        
        # The row and column ranges for iterating from the piece coordinate to the limit coordinate
        row_range = range(piece.row+direction[1], limitRow, direction[1]) if direction[1] != 0 else []
        if direction[1] != 0 and piece.row > limitRow if direction[1] == 1 else limitRow > piece.row:
            raise Exception(f"The row limit {limitRow}, must be {'greater' if direction[1] == 1 else 'lower'} or equal than the piece row '{piece.row}'")
        column_range = range(piece.row+direction[0], limitRow, direction[0]) if direction[0] != 0 else []
        if direction[0] != 0 and piece.column > limitColumn if direction[0] == 1 else limitColumn > piece.column:
            raise Exception(f"The column limit {limitColumn}, must be {'greater' if direction[0] == 1 else 'lower'} or equal than the piece column '{piece.column}'")
        
        #Check if the square is an opponent or if it's a player piece, if not return the limit
        i = 0
        for i, dir in enumerate(zip(row_range, column_range)):
            if self.is_player(dir[0], dir[1], piece.color):
                return i + (1 if includePossibleChecks else 0)

            if self.is_opponent(dir[0], dir[1], piece.color):
                return i+1
            i +=1
            
        return i

    def get_valid_movements(self, piece: Piece, includePossibleChecks: bool = False) -> List[Union[int, int]]:
        """Return all the valid movements of a piece

        Args:
            piece (Piece): Piece to move
            includePossibleChecks (bool, optional): Determine whether it should include movements to pieces of itself. Defaults to False.

        Returns:
            List[Union[int, int]]: List of the valid movements
        """
        
        validMovements = []
        for direction, specialCases in piece.posibleMovements.items():
            movement = (piece.row + direction[1], piece.column + direction[0])
            # If the movement it's out of the boundaries of the board or the square is occupied by a piece of the player, is rejected
            if movement[0] < 0 or movement[1] < 0 or movement[0] > len(ROWS)-1 or movement[1] > len(COLUMNS)-1 or \
            (self.is_player(movement[0], movement[1], piece.color) and not includePossibleChecks):
                continue
            
            # If the movement it's extenable or its a piece with a special movement 
            if piece.extendMovement:
                max_movs = self.get_max_extendable_movements(piece, direction, 8 if direction[1] == 1 else -1, 8 if direction[0] == 1 else -1, includePossibleChecks)
                for i in range(max_movs):
                    validMovements.append((piece.row+(direction[1]*i), piece.column+(direction[0]*i)))                    
            else:
                # Check for special cases
                if (MovementSpecialCase.neitherIsEnemy in specialCases and not self.is_opponent(movement[0], movement[1], piece.color)) or \
                   (MovementSpecialCase.enPassant in specialCases and self.possibleEnPassant is not None and \
                    movement[0] == self.possibleEnPassant[0] and movement[1] == self.possibleEnPassant[1]) or \
                   (MovementSpecialCase.canCastle in specialCases and self.canCastle and self.check == False and \
                    self.get_max_extendable_movements(piece, direction, piece.row, piece.column+(3*direction[1]), includePossibleChecks) == 2 and \
                    (piece.row,piece.column+direction[0]-1) not in self.attackedSquares and \
                    (piece.row,piece.column+direction[0]) not in self.attackedSquares) or \
                   (MovementSpecialCase.doublePawnMove in specialCases and not piece.moved and \
                    self.get_max_extendable_movements(piece, direction, piece.row+(3*direction[1]), piece.column, includePossibleChecks) == 2) or\
                    len(specialCases) == 0:
                        validMovements.append(movement)
                         
        return validMovements

    def move_piece(self, originRow: int, originColumn: int, destinationRow: int, destinationColumn: int) -> bool:
        """Moves a piece from it's origin, to a destination.

        Args:
            originRow (int): Origin row
            originColumn (int): Origin column
            destinationRow (int): Destination row
            destinationColumn (int): Destination column

        Returns:
            bool: Whether the movement was performed or not
        """
        
        piece = self.__grid[originRow][originColumn]
        if (destinationRow, destinationColumn) not in self.get_valid_movements(piece):
            return False

        self.swap_pieces(originRow, originColumn, destinationRow, destinationColumn)
            
        # Check for pawn special cases
        self.possibleEnPassant = None
        if piece.type == PieceType.pawn:
            piece.moved = True
            if piece.row + piece.movingDirection == len(ROWS)-1:
                self.promote_pawn()
                #TODO trigger promotion
                pass

            if abs(destinationRow-originRow) == 2:
                self.possibleEnPassant = (destinationRow - piece.movingDirection, destinationColumn)
                
        self.squares_under_attack()
        self.turn = PlayerColor.black if piece.color == PlayerColor.white else PlayerColor.white
        return True

    #! Development Only method
    def print_board(self):
        for row in range(len(ROWS)):
            for column in range(len(COLUMNS)):
                print(f"{self.__grid[row][column].color.value}{self.__grid[row][column].type.value} ", end='')
            print()

    def serialize(self, filename: str) -> bool:
        """Serializes the board to a json file

        Args:
            filename (str): The name of the json file

        Returns:
            bool: Whether the serialization process was succesfull or not
        """
        
        try:
            with open(f"{SAVINGS}{filename}_board.json", "w") as file:
                data = {
                    'turn' : self.turn.value,
                    'canCastle' : self.canCastle,
                    'possibleEnPassant' : self.possibleEnPassant,
                    '__grid' : [[f"{piece.color.value}{piece.type.value}" for piece in row] for row in self.__grid]
                    }
                json_string = dumps(data, indent=4)
                formatted_json_string = json_string
                removed = 0
                second_char = False
                in_brackets = False
                for i, c in enumerate(json_string):
                    if c == '[':
                        if second_char == False:
                            second_char = True
                            continue
                        in_brackets = True
                    if c == ']':
                        in_brackets = False
                    if in_brackets and (c == '\n' or c == ' '):
                        formatted_json_string = formatted_json_string[:i-removed] + formatted_json_string[i+1-removed:]
                        removed += 1
                
                file.write(formatted_json_string)
            return True
        except Exception as e:
            print(e)
            return False    

    @classmethod
    def deserialize(cls, filename: str) -> object:
        """Deserializes from a json to a Board
        
        Args:
            filename (str): The name of the json file

        Returns:
            Board: Deserialized instance of Board object, or None if failed to deserialize
        """
        
        board = None
        with open(f"{SAVINGS}{filename}_board.json", "r") as file:
            json_data = load(file)
        
            board = cls.start_board(json_data["__grid"])
            board.turn = PlayerColor[json_data['turn']]
            board.canCastle = json_data['canCastle']
            board.possibleEnPassant = tuple(json_data['possibleEnPassant']) if json_data['possibleEnPassant'] != None else None
            
        return board

    @classmethod
    def start_board(cls, textGrid: List[List[str]] = BOARD_START) -> object:
        """Creates a Board object instance, from a string grid, and transforms it to a Piece Object grid

        Args:
            textGrid (List[List[str]], optional): The text grid to transform. Defaults to BOARD_START.

        Returns:
            Board: New instance of Board object
        """
        
        # Parse string matrix to Piece obj matrix, and return Board object
        return cls([[Piece(PieceType[textGrid[row][column][1]], PlayerColor[textGrid[row][column][0]], row, column) for column in range(len(COLUMNS))] for row in range(len(ROWS))])
