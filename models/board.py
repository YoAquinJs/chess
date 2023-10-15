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
        canCastleLeft (bool): Whether castling to left is available for this board or not. Defaults to True.
        canCastleRigth (bool): Whether castling to rigth is available for this board or not. Defaults to True.
        check (bool): Whether the player whoose turn is next is checked or not. Defaults to False.
        turn (PlayerColor): The player whoose turn it's the on going one. Defaults to PlayerColor.white.
        possibleEnPassant (Union[int, int]]): Coordinates of a possible en passant movement for the next turn.
        whitePieces (List[Piece]): List of all pieces of color white.
        blackPieces (List[Piece]): List of all pieces of color black.
        attackedSquares (Union[int, int]]): List of the positions attacked by the opponent pieces in this turn
    """

    def __init__(self, grid: List[List[Piece]], turn: PlayerColor = PlayerColor.white) -> None:
        """Creates a board object instance

        Args:
            __grid (List[List[Piece]]): Grid representing the chess board and the game pieces.
            turn (PlayerColor, optional): Current turn player. Defaults to PlayerColor.white.

        Raises:
            ValueError: When there are no White kings on the board.
            ValueError: When there are no Black kings on the board.
            ValueError: When there are multiple White kings on the board.
            ValueError: When there are multiple Black kings on the board.
        """
        
        self.__grid = grid
        
        # Default board params
        self.canCastleLeft = True
        self.canCastleRigth = True
        
        self.check = False
        self.turn = turn
        self.possibleEnPassant = None
        
        # Buffer Attributes
        self.whitePieces = []
        self.blackPieces = []
        self.attackedSquares = []
        self.whiteKing = None
        self.blackKing = None
        
        # Get all the color pieces in their correspondent lists
        for row in range(len(ROWS)):
            for column in range(len(COLUMNS)):
                piece = self.__grid[row][column]
                
                if piece.type == PieceType.king:
                    if piece.color == PlayerColor.white:
                        if self.whiteKing != None:
                            raise ValueError("There are multiple white kings in this board")
                        self.whiteKing = piece
                    else:
                        if self.blackKing != None:
                            raise ValueError("There are multiple black kings in this board")
                        self.blackKing = piece
                elif piece.type != PieceType.empty:
                    self.whitePieces.append(piece) if piece.color == PlayerColor.white else self.blackPieces.append(piece)
                    
        if self.whiteKing == None:
            raise ValueError("There is no white king in this board")
        if self.blackKing == None:
            raise ValueError("There is no black king in this board")
        
        self.squares_under_attack(PlayerColor.black if self.turn == PlayerColor.white else PlayerColor.white)
        self.in_check()

    def square(self, row: int, column: int) -> Piece:
        """Returns the piece in the specified square

        Args:
            row (int): Specified row
            column (int): Specified column

        Returns:
            Piece: Piece in the square
        """
        
        return self.__grid[row][column]

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

    def empty_square(self, row: int, column: int):
        """Empty the specified square

        Args:
            row (int): Row of the square.
            column (int): Column of the square.
        """
        self.__grid[row][column] = Piece(PieceType.empty, PlayerColor.empty, row, column)

    def squares_under_attack(self, opponent: PlayerColor):
        """Calculate the squares under attack by the opponent pieces

        Args:
            opponent (PlayerColor): Opponent color.
        """

        self.attackedSquares = []
        
        opponentPieces = self.whitePieces if opponent == PlayerColor.white else self.blackPieces
        # iterate trougth all the opponent pieces, and determine if anyone can move to the desired square
        for piece in opponentPieces:
            for movement in self.get_valid_movements(piece, True):
                if piece.type == PieceType.pawn and piece.column == movement[1]:
                    continue
                
                if movement not in self.attackedSquares:
                    self.attackedSquares.append(movement)

#TODO Validate when check if it's a checkmate\
    def in_check(self):
        """Evaluates if the player whoose turn is next is in check
        """
        
        playerKing = self.whiteKing if self.turn == PlayerColor.white else self.blackKing
        self.check = (playerKing.row, playerKing.column) in self.attackedSquares

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

    def get_max_extendable_movements(self, piece: Piece, direction: Union[int, int], maxIterations: int = 8) -> int:
        """Given a piece and direction, returns the number of movements it can perform before reaching a given limit

        Args:
            piece (Piece): Piece to move.
            direction (Union[int, int]): Direction of the extenable movement.
            maxIterations(int, optional): Maximum distance from piece origin. Defaults to 8.
            
        Returns:
           Int: Maximun number of movements in that direction.
        """
        
        #// The row and column ranges for iterating from the piece coordinate to the limit coordinate
        #//row_range = range(piece.row+direction[1], limitRow, direction[1]) if direction[1] != 0 else []
        #//if direction[1] != 0 and piece.row > limitRow if direction[1] == 1 else limitRow > piece.row:
        #//    raise Exception(f"The row limit {limitRow}, must be {'greater' if direction[1] == 1 else 'lower'} or equal than the piece row '{piece.row}'")
        #//column_range = range(piece.row+direction[0], limitRow, direction[0]) if direction[0] != 0 else []
        #//if direction[0] != 0 and piece.column > limitColumn if direction[0] == 1 else limitColumn > piece.column:
        #//    raise Exception(f"The column limit {limitColumn}, must be {'greater' if direction[0] == 1 else 'lower'} or equal than the piece column '{piece.column}'")
        
        i = 0
        row = piece.row
        column = piece.column
        #//for i, dir in enumerate(zip(row_range, column_range)):
        while (row > -1 and row < 8) and (column > -1 and column < 8) and i < maxIterations:
            row += direction[0]
            column += direction[1]
            
            #Check if the square is an opponent or if it's a player piece, if not return the limit
            if row < 0 or row > 7 or column < 0  or column > 7 or self.is_player(row, column, piece.color):
                return i

            if self.is_opponent(row, column, piece.color):
                return i+1
            
            i +=1
            
        return i

    def get_valid_movements(self, piece: Piece, countPawnAttacks: bool = False) -> List[Union[int, int]]:
        """Return all the valid movements of a piece

        Args:
            piece (Piece): Piece to move
            countPawnAttacks (bool, optional): Determine whether to count the possible pawn attacks (used for the attacked squares calculation). Defaults to False.

        Returns:
            List[Union[int, int]]: List of the valid movements
        """
        
        validMovements = []

        for direction, specialCase in piece.posibleMovements.items():
            for i in range(1,self.get_max_extendable_movements(piece, direction, piece.maxExtend)+1):
                movement = (piece.row + (direction[0]*i), piece.column + (direction[1]*i))
                # Check for special cases
                if piece.type == PieceType.pawn:
                    if specialCase == MovementSpecialCase.doublePawnMove and\
                        ((piece.row == 1 and piece.color == PlayerColor.black) or (piece.row == 6 and piece.color == PlayerColor.white))\
                        and self.__grid[piece.row + int(direction[0]/2)][movement[1]].type == PieceType.empty and self.__grid[movement[0]][movement[1]].type == PieceType.empty:
                        validMovements.append(movement)
                    elif specialCase == MovementSpecialCase.isEmpty and self.__grid[movement[0]][movement[1]].type == PieceType.empty:
                        validMovements.append(movement)
                    elif specialCase == None and (self.is_opponent(movement[0], movement[1], piece.color) or countPawnAttacks or movement == self.possibleEnPassant):
                        validMovements.append(movement)
                elif specialCase == MovementSpecialCase.canCastle and (piece.row, piece.column + (direction[1]/2)) not in self.attackedSquares\
                    and (self.canCastleLeft if direction[1] < 0 else self.canCastleRigth):
                    validMovements.append(movement)
                elif specialCase == None:
                    validMovements.append(movement)

        return validMovements
                #//if (MovementSpecialCase.neitherIsEnemy in specialCases and not self.is_opponent(movement[0], movement[1], piece.color)) or \
                #//   (MovementSpecialCase.enPassant in specialCases and self.possibleEnPassant is not None and \
                #//    movement[0] == self.possibleEnPassant[0] and movement[1] == self.possibleEnPassant[1]) or \
                #//   (MovementSpecialCase.canCastleLeft in specialCases and self.canCastle and self.check == False and \
                #//    self.get_max_extendable_movements(piece, direction, includePossibleChecks, 2) == 2 and \
                #//    (piece.row,piece.column+direction[0]-1) not in self.attackedSquares and \
                #//    (piece.row,piece.column+direction[0]) not in self.attackedSquares) or \
                #//   (MovementSpecialCase.doublePawnMove in specialCases and not piece.moved and \
                #//    self.get_max_extendable_movements(piece, direction, includePossibleChecks, 2) == 2) or\
                #//    len(specialCases) == 0:
                #//        validMovements.append(movement)                         
    
    def is_valid_movement(self, originRow: int, originColumn: int, destinationRow: int, destinationColumn: int) -> bool:
        """Determines whether the piece movement is valid or not

        Args:
            originRow (int): Origin row
            originColumn (int): Origin column
            destinationRow (int): Destination row
            destinationColumn (int): Destination column

        Returns:
            bool: Whether the movement is valid or not.
        """
        
        piece = self.__grid[originRow][originColumn]
        
        # If you try to move an empty square
        if piece.type == PieceType.empty:
            return False
        
        # If you try to move an opponent square
        if self.is_opponent(originRow, originColumn, self.turn):
            return False
        
        # If the movement is an ilegal movement
        if (destinationRow, destinationColumn) not in self.get_valid_movements(piece):
            return False

        # Perform movement and determine if player was left in check
        self.swap_pieces(originRow, originColumn, destinationRow, destinationColumn)
        self.squares_under_attack(PlayerColor.black if piece.color == PlayerColor.white else PlayerColor.white)
        self.in_check()
        
        # Discard movement
        self.swap_pieces(destinationRow, destinationColumn, originRow, originColumn)
        
        # If player left in check is invalid
        if self.check:
            return False
        
        return True

#TODO check if only kings left
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
        
        # If you try to move an empty square
        if not self.is_valid_movement(originRow, originColumn,destinationRow, destinationColumn):
            return False
        
        piece = self.__grid[originRow][originColumn]
        self.swap_pieces(originRow,originColumn,destinationRow,destinationColumn)
        
        # Check for pawn special cases
        self.possibleEnPassant = None
        if piece.type == PieceType.pawn:
            if piece.row + piece.movingDirection == len(ROWS)-1:
                self.promote_pawn()
                #TODO trigger promotion
                pass

            if abs(destinationRow-originRow) == 2:
                self.possibleEnPassant = (destinationRow - piece.movingDirection, destinationColumn)
                
        self.squares_under_attack(self.turn)
        self.turn = PlayerColor.black if piece.color == PlayerColor.white else PlayerColor.white
        self.in_check()

        return True

    def print_board(self): #! Development Only method
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
                    'canCastleLeft' : self.canCastleLeft,
                    'canCastleRigth' : self.canCastleRigth,
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
        
            board = cls.start_board(json_data["__grid"], PlayerColor[json_data['turn']])
            board.canCastleRigth = json_data['canCastleRigth']
            board.canCastleLeft = json_data['canCastleLeft']
            board.possibleEnPassant = tuple(json_data['possibleEnPassant']) if json_data['possibleEnPassant'] != None else None
        return board

    @classmethod
    def start_board(cls, textGrid: List[List[str]] = BOARD_START, turn: PlayerColor = PlayerColor.white) -> object:
        """Creates a Board object instance, from a string grid, and transforms it to a Piece Object grid

        Args:
            textGrid (List[List[str]], optional): The text grid to transform. Defaults to BOARD_START.
            turn (PlayerColor, optional): Current turn player. Defaults to PlayerColor.white.

        Returns:
            Board: New instance of Board object
        """
        
        # Parse string matrix to Piece obj matrix, and return Board object
        return cls([[Piece(PieceType[textGrid[row][column][1]], PlayerColor[textGrid[row][column][0]], row, column) for column in range(len(COLUMNS))] for row in range(len(ROWS))], turn)
