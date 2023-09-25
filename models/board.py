"""This module contains the Board model object"""
import sys
from json import dumps, load
from typing import Dict, Union, List

from models.consts import PieceType, PlayerColor, MovementSpecialCase, COLUMNS, ROWS, BOARD_START, SAVINGS
from models.piece import Piece

class Board():
    """Class for handling game screens, and game states

    Attributes:
        __grid (List[List[Piece]]): Grid representing the board configuration, it's private
    """

    def __init__(self, grid: List[List[Piece]], can_castle: bool = True) -> None:
        """Creates a board object instance

        Args:
            __grid (List[List[Piece]]): Grid representing the chess board and the game pieces.
            can_castle (bool, optional): Whether castling is available for this board or not. Defaults to True.
        """
        
        self.__grid = grid
        self.can_castle = can_castle
        self.rows = ROWS
        self.columns = COLUMNS
        
        self.whitePieces = []
        self.blackPieces = []
        
        for row in range(len(ROWS)):
            for column in range(len(COLUMNS)):
                piece = self.__grid[row][column]
                if piece.type != PieceType.empty:
                    self.whitePieces.append(piece) if piece.color == PlayerColor.white else self.blackPieces.append(piece)
                    
    def is_empty(self, row: int, column: int) -> bool:
        """Returns whether the square is empty or not

        Args:
            row (int): Row
            column (int): Column

        Returns:
            bool: Empty or not
        """
        
        return self.__grid[row][column].type == PieceType.empty
                
    def is_enemy(self, row: int, column: int, playerColor: PlayerColor) -> bool:
        """Returns whether the square is ocuppied by an opponent piece or not

        Args:
            row (int): Row
            column (int): Column
            playerColor(PlayerColor): The player which is checking for the opponent color

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].type != PieceType.empty and self.__grid[row][column].color != playerColor
    
    def swap_pieces(self, row1: int, column1: int, row2: int, column2: int):
        """Swap the piece from the square 1, with the piece with the square 2

        Args:
            row1 (int): Row for square 1
            column1 (int): column for square 1
            row2 (int): Row for square 2
            column2 (int): column for square 2
        """
        
        self.__grid[row1][column1], self.__grid[row2][column2] = self.__grid[row2][column2], self.__grid[row1][column1]
        
    def get_valid_movements(self, piece: Piece) -> List[Union[int, int]]:
        """Return all the valid movements of a piece

        Args:
            piece (Piece): Piece to move

        Returns:
            List[Union[int, int]]: List of the valid movements
        """
        
        validMovements = []
        for direction, specialCases in piece.posibleMovements.items():
            movement = (piece.row + direction[1], piece.column + direction[0])
            if movement[0] < 0 or movement[1] < 0 or movement[0] > len(ROWS)-1 or movement[1] > len(COLUMNS)-1:
                continue
            
            if piece.extendMovement:
                validMovements.append(movement)
            else:
                if MovementSpecialCase.canCastle in specialCases and self.can_castle:
                    validMovements.append(movement)
                if MovementSpecialCase.doublePawnMove in specialCases and not piece.moved:
                    #TODO Register for enPassant
                    validMovements.append(movement)
                if MovementSpecialCase.isEnemy in specialCases and self.is_enemy(movement[0], movement[1]):
                    validMovements.append(movement)
                elif MovementSpecialCase.enPassant in specialCases: #TODO enPassant validation
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
        if Union[destinationRow, destinationColumn] in self.get_valid_movements(piece):
            self.swap_pieces(originRow, originColumn, destinationRow, destinationColumn)
            piece.row = destinationRow
            piece.column = destinationColumn
            
            if piece.type == PieceType.pawn:
                piece.moved = True
                if piece.row + next(key for key, value in piece.posibleMovements.items() if value == [])[1] > len(ROWS)-1:
                    #TODO promotion
                    pass
            
            return True
            
        return False
    
    #//! Development Only method
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
            with open(f"{SAVINGS}{filename}.json", "w") as file:
                data = {
                    'can_castle' : self.can_castle,
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
        with open(f"{SAVINGS}{filename}.json", "r") as file:
            json_data = load(file)
        
            board = cls.start_board(json_data["__grid"])
            for attr, value in json_data.items():
                if attr == '__grid':
                    continue
                setattr(board, attr, value)
                
        return board
    
    @classmethod
    def start_board(cls, textGrid: List[List[str]] = BOARD_START) -> object:
        """Creates a Board object instance, from a string grid, and transforms it to a Piece Object grid

        Args:
            textGrid (List[List[str]], optional): The text grid to transform. Defaults to BOARD_START.

        Returns:
            Board: New instance of Board object
        """
        
        return cls([[Piece(PieceType[textGrid[row][column][1]], PlayerColor[textGrid[row][column][0]], row, column) for column in range(len(COLUMNS))] for row in range(len(ROWS))])