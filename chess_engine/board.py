"""This module contains the Board model object and it's properties"""

from copy import deepcopy
from json import dumps, load
from typing import Dict, Union, List
from asyncio import run

from utils.utils import color_print, opponent
from chess_engine.piece import Piece
from core.consts import PieceType, PlayerColor, MovementSpecialCase, PrintColor, BoardState, COLUMNS, ROWS, BOARD_START, SAVINGS

class Board():
    """Class for handling game screens, and game states

    Attributes:
        __grid (List[List[Piece]]): Grid representing the board configuration, it's private
        getPromotionPiece(function): Asynchronous function for getting the piece on promotion.
        canCastleLeft (bool): Whether castling to left is available for this board or not. Defaults to True.
        canCastleRigth (bool): Whether castling to rigth is available for this board or not. Defaults to True.
        boardState (BoardState): The game state of the board. Defaults to BoardState.moveTurn.
        turn (PlayerColor): The player whoose turn it's the on going one. Defaults to PlayerColor.white.
        possibleEnPassant (Union[int, int]]): Coordinates of a possible en passant movement for the next turn.
        whitePieces (Dict[Piece,List[Union(int,int)]]): List of all pieces of color white.
        blackPieces (Dict[Piece,List[Union(int,int)]]): List of all pieces of color black.
        whiteKing (piece): White king piece object reference.
        blackKing (piece): Black king piece object reference.
    """

    def __init__(self, grid: List[List[Piece]], turn: PlayerColor = PlayerColor.white, afterMoveCheck: bool = False) -> None:
        """Creates a board object instance

        Args:
            __grid (List[List[Piece]]): Grid representing the chess board and the game pieces.
            turn (PlayerColor, optional): Current turn player. Defaults to PlayerColor.white.
            afterMoveCheck (bool, optional): Whether to not determine if the current board is checkmate or stalemate. Defaults to false.

        Raises:
            ValueError: When there are no White kings on the board.
            ValueError: When there are no Black kings on the board.
            ValueError: When there are multiple White kings on the board.
            ValueError: When there are multiple Black kings on the board.
        """
        
        self.__grid = grid
        self.getPromotionPiece = None
        
        # Default board params
        self.canCastleLeft = True
        self.canCastleRigth = True
        
        self.boardState = BoardState.moveTurn
        self.turn = turn
        self.possibleEnPassant = None
        
        self.whiteKing = None
        self.blackKing = None
        self.whitePieces = {}
        self.blackPieces = {}
        
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
                    if piece.color == PlayerColor.white:
                        self.whitePieces[piece] = []
                    else:
                        self.blackPieces[piece] = []
                    
        if self.whiteKing == None:
            raise ValueError("There is no white king in this board")
        if self.blackKing == None:
            raise ValueError("There is no black king in this board")
        
        self.squares_under_attack(opponent(self.turn))
        self.get_posible_turn_movements()
        self.set_game_state(afterMoveCheck)

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
            row (int): Row.
            column (int): Column.
            playerColor(PlayerColor): The opponent color.

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].color == opponent(playerColor)

    def is_player(self, row: int, column: int, playerColor: PlayerColor) -> bool:
        """Returns whether the square is ocuppied by a piece of the player or not

        Args:
            row (int): Row
            column (int): Column
            playerColor(PlayerColor): The player which is checking for it's color

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].color == playerColor

    def is_attacked(self, row: int, column: int, opponent: PlayerColor) -> bool:
        """Determines if the specified square is attacked by the opponent or not

        Args:
            row (int): Square row.
            column (int): Square column.
            opponent (PlayerColor): Opponent that is attacking.

        Returns:
            bool: Whether the square is attacked or not
        """
        
        opponentPieces = self.whitePieces if opponent == PlayerColor.white else self.blackPieces
        return any((row,column) in attackedSquares for attackedSquares in opponentPieces.values())

    def empty_square(self, row: int, column: int):
        """Empty the specified square

        Args:
            row (int): Row of the square.
            column (int): Column of the square.
        """
        self.__grid[row][column] = Piece(PieceType.empty, PlayerColor.empty, row, column)

    def add_piece(self, row: int, column: int, piece: Piece) -> bool:
        """Adds a piece to the board if the square is empty

        Args:
            row (int): Row where the piece will be added.
            column (int): Column where the piece will be added.
            piece (Piece): Piece to be addded.

        Returns:
            bool: Whether the piece was added or not
        """
        
        if self.__grid[row][column].type != PieceType.empty:
            color_print(f"The piece {piece.color}{piece.type} is trying to be added in {(row,column)}, where piece {self.__grid[row][column].type}{self.__grid[row][column].type} is", PrintColor.yellow)
            return False
        
        if piece.color == PlayerColor.white:
            self.whitePieces[piece] = []
        else:
            self.blackPieces[piece] = []
        self.__grid[row][column] = piece
        return True
    
    def remove_piece(self, row: int, column: int) -> bool:
        """Removes a piece from the board if the square is not empty

        Args:
            row (int): Row where the piece will be removed.
            column (int): Column where the piece will be removed.

        Returns:
            bool: Whether the piece was removed or not
        """
        
        if self.__grid[row][column].type == PieceType.empty:
            color_print(f"An empty square {(row,column)} is trying be removed", PrintColor.yellow)
            return False
        
        if self.__grid[row][column].color == PlayerColor.white:
            self.whitePieces.pop(self.__grid[row][column], None)
        else:
            self.blackPieces.pop(self.__grid[row][column], None)
        self.empty_square(row, column)
        return True

    def squares_under_attack(self, opponent: PlayerColor):
        """Calculate the squares under attack by the opponent pieces

        Args:
            opponent (PlayerColor): Opponent color.
        """

        opponentPieces = self.whitePieces if opponent == PlayerColor.white else self.blackPieces
        
        for piece, posibleMovs in opponentPieces.items():
            posibleMovs.clear()
            for movement in self.get_valid_movements(piece, True):
                if piece.type != PieceType.pawn:
                    posibleMovs.append(movement)
                elif piece.column != movement[1]:
                    posibleMovs.append(movement)

    def get_posible_turn_movements(self, turn: PlayerColor = None):
        """Calculate the squares wich the turn pieces can move to

        Args:
            turn (PlayerColor, optional): Player turn. Defaults to None.
        """
        
        if turn == None:
            turn = self.turn
        
        playerPieces = self.whitePieces if turn == PlayerColor.white else self.blackPieces
        
        for piece, posibleMovs in playerPieces.items():
            posibleMovs.clear()
            for movement in self.get_valid_movements(piece, True):
                posibleMovs.append(movement)

    def set_game_state(self, afterMoveCheck: bool = False):
        """Evaluates if the player whoose turn is next is in check, and if it's checkmate or stalemate
        
        Args:
            afterMoveCheck (bool, optional): Whether to not determine if the current board is checkmate or stalemate. Defaults to false.
        """
        
        playerKing = self.whiteKing if self.turn == PlayerColor.white else self.blackKing
        inCheck = self.is_attacked(playerKing.row, playerKing.column, opponent(self.turn))
        
        if afterMoveCheck:
            self.boardState = BoardState.check if inCheck else BoardState.moveTurn
            return

        playerPieces = self.whitePieces if self.turn == PlayerColor.white else self.blackPieces
        anyValidMov = False
        for piece, posibleMovs in playerPieces.items():
            if any((not self.in_check_after_mov(piece.row, piece.column, mov[0], mov[1])) for mov in posibleMovs):
                anyValidMov = True
                break
                
        if not anyValidMov and inCheck:
            self.boardState = BoardState.checkmate
        elif inCheck:
            self.boardState = BoardState.check
        elif not anyValidMov:
            self.boardState = BoardState.stalemate
        else:
            self.boardState = BoardState.moveTurn
                        
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
        
        i = 0
        row = piece.row
        column = piece.column

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

    def in_check_after_mov(self, originRow: int, originColumn: int, destinationRow: int, destinationColumn: int) -> bool:
        """Determines if after this movement is executed the player is left in check or not

        Args:
            originRow (int): Origin row
            originColumn (int): Origin column
            destinationRow (int): Destination row
            destinationColumn (int): Destination column

        Returns:
            bool: Whether the player is left in check or not
        """
        
        piece = self.__grid[originRow][originColumn]
        
        eatenPiece = None
        if self.__grid[destinationRow][destinationColumn].type != PieceType.empty:
            eatenPiece = self.__grid[destinationRow][destinationColumn]

        # If move was enPassant
        enPassant = piece.type == PieceType.pawn and self.possibleEnPassant != None and self.possibleEnPassant[0] == destinationRow and self.possibleEnPassant[1] == destinationColumn
        if enPassant:
            eatenPiece = self.__grid[destinationRow-piece.movingDirection][destinationColumn]

        if eatenPiece != None:
            self.remove_piece(eatenPiece.row, eatenPiece.column)
            
        self.swap_pieces(originRow, originColumn, destinationRow, destinationColumn)
        hipothetycalBoard = Board(deepcopy(self.__grid), self.turn, True)
        self.swap_pieces(destinationRow, destinationColumn, originRow, originColumn)
        if eatenPiece != None:
            self.add_piece(destinationRow if not enPassant else destinationRow-piece.movingDirection, destinationColumn, eatenPiece)

        return hipothetycalBoard.boardState == BoardState.check or hipothetycalBoard.boardState == BoardState.checkmate

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
                        and self.__grid[piece.row + int(direction[0]//2)][movement[1]].type == PieceType.empty and self.__grid[movement[0]][movement[1]].type == PieceType.empty:
                        validMovements.append(movement)
                    elif specialCase == MovementSpecialCase.isEmpty and self.__grid[movement[0]][movement[1]].type == PieceType.empty:
                        validMovements.append(movement)
                    elif specialCase == None and (self.is_opponent(movement[0], movement[1], piece.color) or countPawnAttacks or movement == self.possibleEnPassant):
                        validMovements.append(movement)
                elif specialCase == MovementSpecialCase.castle and not self.is_attacked(piece.row, piece.column + (direction[1]//2),opponent(piece))\
                    and self.__grid[piece.row][ piece.column + (direction[1]//2)].type == PieceType.empty\
                    and (self.canCastleLeft if direction[1] < 0 else self.canCastleRigth) and self.boardState != BoardState.check:
                    validMovements.append(movement)
                elif specialCase == None:
                    validMovements.append(movement)

        return validMovements
    
    def is_valid_movement(self, originRow: int, originColumn: int, destinationRow: int, destinationColumn: int, alreadyValidated: bool = False) -> bool:
        """Determines whether the piece movement is valid or not

        Args:
            originRow (int): Origin row
            originColumn (int): Origin column
            destinationRow (int): Destination row
            destinationColumn (int): Destination column
            alreadyValidated (bool, optional): Determine if it should validate it with get_valid_movements(). Defaults to False.

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
        if not alreadyValidated and (destinationRow, destinationColumn) not in self.get_valid_movements(piece):
            return False

        # If the movement leave you in check
        if self.in_check_after_mov(originRow, originColumn, destinationRow, destinationColumn):
            return False
        
        return True

    def attempt_move(self, originRow: int, originColumn: int, destinationRow: int, destinationColumn: int) -> Union[bool, dict]:
        """Moves a piece from it's origin, to a destination.

        Args:
            originRow (int): Origin row.
            originColumn (int): Origin column.
            destinationRow (int): Destination row.
            destinationColumn (int): Destination column.

        Returns:
            bool: Whether the movement was performed or not.
            dict: Dictionary containing info on the performed move, or None if no move was performed.
        """
        
        # If you try to move an empty square
        if not self.is_valid_movement(originRow, originColumn,destinationRow, destinationColumn):
            return False, None
        
        eatPiece = self.__grid[destinationRow][destinationColumn]

        piece = self.__grid[originRow][originColumn]
        self.swap_pieces(originRow,originColumn,destinationRow,destinationColumn)        
            
        # Check for pawn special cases
        possibleEnPassant = None
        if piece.type == PieceType.pawn:
            # If move was enPassant
            if self.possibleEnPassant != None and self.possibleEnPassant[0] == destinationRow and self.possibleEnPassant[1] == destinationColumn:
                eatPiece = self.__grid[destinationRow-piece.movingDirection][destinationColumn]
            # If pawn performed doublemove, save it for en passant
            elif abs(destinationRow-originRow) == 2:
                possibleEnPassant = (destinationRow - piece.movingDirection, destinationColumn)
            # If pawn reached the last square it can move, promote it
            elif piece.row + piece.movingDirection == len(ROWS) or piece.row + piece.movingDirection == -1:
                self.remove_piece(piece.row, piece.column)
                if self.getPromotionPiece == None:
                    raise Exception("getPromotionPiece function not yet defined for board")
                newPiece = run(self.getPromotionPiece())
                self.add_piece(piece.row,piece.column, newPiece)
        elif piece.type == PieceType.king:
            self.canCastleLeft = False
            self.canCastleRigth = False
            # If move was castle
            if abs(destinationColumn-originColumn) == 2:
                direction = (destinationColumn-originColumn)//abs(destinationColumn-originColumn)
                self.swap_pieces(originRow, 0 if direction == -1 else 7, originRow, destinationColumn - direction)
        
        self.possibleEnPassant = possibleEnPassant
        
        # Eat opponent piece if it's eat move
        if eatPiece.type != PieceType.empty:
            self.empty_square(eatPiece.row, eatPiece.column)

        self.turn = opponent(self.turn)
        self.squares_under_attack(opponent(self.turn))
        self.get_posible_turn_movements()
        self.set_game_state()

        return True, {
            'piece': piece,
            'eatPiece': eatPiece if eatPiece.type !=PieceType.empty else None
        }

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
