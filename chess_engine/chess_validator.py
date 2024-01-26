"""This module contains the Board model object and it's properties"""

# Import external libraries
from __future__ import annotations

from asyncio import run
from copy import deepcopy
from typing import Any, Optional

from chess_engine.piece import Piece
from game_logic.consts import (COLUMNS, ROWS, BoardState,
                               MovSpecialCase, PieceType, PlayerColor,
                               PrintColor)
from serialization.serializable import Serializable
# Import Internal modules
from utils.utils import color_print, opponent


class ChessValidator(Serializable):
    """TODO
    """

    fileEnd = '_b.json'

    def __init__(self, grid: list[list[Piece]], turn: PlayerColor = PlayerColor.WHITE, afterMoveCheck: bool = False):
        self.__grid = grid
        self.get_promotion_piece = None

        # Default board params
        self.canCastleLeft = True
        self.canCastleRigth = True

        self.boardState = BoardState.MOVE_TURN
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

                if piece.type == PieceType.KING:
                    if piece.color == PlayerColor.WHITE:
                        if self.whiteKing != None:
                            raise ValueError("There are multiple white kings in this board")
                        self.whiteKing = piece
                    else:
                        if self.blackKing != None:
                            raise ValueError("There are multiple black kings in this board")
                        self.blackKing = piece

                if piece.type != PieceType.EMPTY:
                    if piece.color == PlayerColor.WHITE:
                        self.whitePieces[piece] = []
                    else:
                        self.blackPieces[piece] = []

        if self.whiteKing == None:
            raise ValueError("There is no white king in this board")
        if self.blackKing == None:
            raise ValueError("There is no black king in this board")

        # Set turn conditions
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
            playerColor(PlayerColor): The player color.

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
        
        opponentPieces = self.whitePieces if opponent == PlayerColor.WHITE else self.blackPieces
        return any((row,column) in attackedSquares for attackedSquares in opponentPieces.values())

    def empty_square(self, row: int, column: int) -> None:
        """Empty the specified square

        Args:
            row (int): Row of the square.
            column (int): Column of the square.
        """
        
        self.__grid[row][column] = Piece(PieceType.EMPTY, PlayerColor.EMPTY, row, column)

    def add_piece(self, row: int, column: int, piece: Piece) -> bool:
        """Adds a piece to the board if the square is empty

        Args:
            row (int): Row where the piece will be added.
            column (int): Column where the piece will be added.
            piece (Piece): Piece to be addded.

        Returns:
            bool: Whether the piece was added or not
        """
        
        if self.__grid[row][column].type != PieceType.EMPTY:
            color_print(f"The piece {piece.color}{piece.type} is trying to be added in {(row,column)}, where piece {self.__grid[row][column].type}{self.__grid[row][column].type} is", PrintColor.YELLOW)
            return False
        
        if piece.color == PlayerColor.WHITE:
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

        if self.__grid[row][column].type == PieceType.EMPTY:
            color_print(f"An empty square {(row,column)} is trying be removed", PrintColor.YELLOW)
            return False
        
        if self.__grid[row][column].color == PlayerColor.WHITE:
            self.whitePieces.pop(self.__grid[row][column], None)
        else:
            self.blackPieces.pop(self.__grid[row][column], None)
        self.empty_square(row, column)
        
        return True

    def squares_under_attack(self, opponent: PlayerColor) -> None:
        """Calculate the squares under attack by the opponent pieces

        Args:
            opponent (PlayerColor): Opponent color.
        """

        opponentPieces = self.whitePieces if opponent == PlayerColor.WHITE else self.blackPieces
        
        for piece, posibleMovs in opponentPieces.items():
            posibleMovs.clear()
            for movement in self.get_valid_movements(piece, True):
                if piece.type != PieceType.PAWN:
                    posibleMovs.append(movement)
                elif piece.column != movement[1]: # If the movement is different to pawn frontal move, add it
                    posibleMovs.append(movement)

    def get_posible_turn_movements(self, turn: PlayerColor = None) -> None:
        """Calculate the squares which the turn pieces can move to

        Args:
            turn (PlayerColor, optional): Player turn. Defaults to None.
        """
        
        if turn == None:
            turn = self.turn
        
        playerPieces = self.whitePieces if turn == PlayerColor.WHITE else self.blackPieces
        
        for piece, posibleMovs in playerPieces.items():
            posibleMovs.clear()
            posibleMovs += self.get_valid_movements(piece)

    def set_game_state(self, afterMoveCheck: bool = False) -> None:
        """Evaluates if the board state of the player whoose turn is next
        
        Args:
            afterMoveCheck (bool, optional): Whether to not determine if the current board is checkmate or stalemate, used for avoiding infinite recursion loops. Defaults to false.
        """
        
        playerKing = self.whiteKing if self.turn == PlayerColor.WHITE else self.blackKing
        inCheck = self.is_attacked(playerKing.row, playerKing.column, opponent(self.turn))
        
        # Check whether to continuo with stalemate or checkmate validation
        if afterMoveCheck:
            self.boardState = BoardState.CHECK if inCheck else BoardState.MOVE_TURN
            return
        
        # If only kings left in board, mark stalemate
        if len(self.whitePieces) == 1 and len(self.blackPieces == 1):
            self.boardState = BoardState.STALEMATE
            return

        # Validate if the player has any legal movement available, if not it's either stalemate or checkmate
        anyValidMov = False
        playerPieces = self.whitePieces if self.turn == PlayerColor.WHITE else self.blackPieces
        for piece, posibleMovs in playerPieces.items():
            if any((not self.in_check_after_mov(piece.row, piece.column, mov[0], mov[1])) for mov in posibleMovs):
                anyValidMov = True
                break
                
        # Set board state
        if not anyValidMov and inCheck:
            self.boardState = BoardState.CHECKMATE
        elif inCheck:
            self.boardState = BoardState.CHECK
        elif not anyValidMov:
            self.boardState = BoardState.STALEMATE
        else:
            self.boardState = BoardState.MOVE_TURN

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

    def get_max_extendable_movements(self, piece: Piece, direction: tuple[int, int], maxIterations: int) -> int:
        """Given a piece and direction, returns the number of movements it can perform without colliding, before reaching a given limit

        Args:
            piece (Piece): Piece to move.
            direction (tuple[int, int]): Direction of the extenable movement.
            maxIterations(int, optional): Maximum distance from piece origin.
            
        Returns:
           Int: Maximun number of movements in that direction.
        """
        
        i = 0
        row = piece.row
        column = piece.column

        while (row > -1 and row < 8) and (column > -1 and column < 8) and i < maxIterations:
            row += direction[0]
            column += direction[1]
            
            #If square is off board limits, or collided with a player piece return the previous square
            if row < 0 or row > 7 or column < 0  or column > 7 or self.is_player(row, column, piece.color):
                return i

            # If square is opponent return until this square
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
        
        # Get the eaten piece to remove it for calculations, and add it after the calculations are performed
        eatenPiece = None
        if self.__grid[destinationRow][destinationColumn].type != PieceType.EMPTY:
            eatenPiece = self.__grid[destinationRow][destinationColumn]

        # If move was enPassant
        enPassant = piece.type == PieceType.PAWN and self.possibleEnPassant != None and self.possibleEnPassant[0] == destinationRow and self.possibleEnPassant[1] == destinationColumn
        if enPassant:
            eatenPiece = self.__grid[destinationRow-piece.moving_dir][destinationColumn]

        if eatenPiece != None:
            self.remove_piece(eatenPiece.row, eatenPiece.column)
            
        # Perform the movement, create a new board with this new grid, and in that board determine if the player is in check after the movement, then undo the movement
        self.swap_pieces(originRow, originColumn, destinationRow, destinationColumn)
        hipothetycalBoard = ChessValidator(deepcopy(self.__grid), self.turn, True)
        self.swap_pieces(destinationRow, destinationColumn, originRow, originColumn)
        
        # Add the eaten piece if there's one
        if eatenPiece != None:
            self.add_piece(destinationRow if not enPassant else destinationRow-piece.moving_dir, destinationColumn, eatenPiece)

        return hipothetycalBoard.boardState == BoardState.CHECK or hipothetycalBoard.boardState == BoardState.CHECKMATE

    def get_valid_movements(self, piece: Piece, countPawnAttacks: bool = False) -> list[tuple[int, int]]:
        """Return all the valid movements of a piece

        Args:
            piece (Piece): Piece to move
            countPawnAttacks (bool, optional): Determine whether to count the possible pawn attacks (used for the attacked squares calculation). Defaults to False.

        Returns:
            list[tuple[int, int]]: list of the valid movements
        """
        
        validMovements = []

        # Iterate trougth the posible movement os each piece
        for direction, specialCase in piece.movements.items():
            for i in range(1,self.get_max_extendable_movements(piece, direction, piece.max_extend)+1):
                movement = (piece.row + (direction[0]*i), piece.column + (direction[1]*i))
                
                # Check for pawn special cases
                if piece.type == PieceType.PAWN:
                    # Verify pawn in it's initial row, and that it's path is empty, for double pawn move
                    if specialCase == MovSpecialCase.DOUBLE_PAWN_MOVE and\
                        ((piece.row == 1 and piece.color == PlayerColor.BLACK) or (piece.row == 6 and piece.color == PlayerColor.WHITE))\
                        and self.__grid[piece.row + int(direction[0]//2)][movement[1]].type == PieceType.EMPTY and self.__grid[movement[0]][movement[1]].type == PieceType.EMPTY:
                        validMovements.append(movement)
                    # Verify that pawn's path is empty in normal movement
                    elif specialCase == MovSpecialCase.IS_EMPTY and self.__grid[movement[0]][movement[1]].type == PieceType.EMPTY:
                        validMovements.append(movement)
                    # Verify that the attacking square is either an enemy, enpassant or countPawnAttacks set to true
                    elif specialCase == None and (countPawnAttacks or self.is_opponent(movement[0], movement[1], piece.color) or movement == self.possibleEnPassant):
                        validMovements.append(movement)
                # Verify castling is available, path is empty and not attacked, and king not in check
                elif specialCase == MovSpecialCase.CASTLE and not self.is_attacked(piece.row, piece.column + (direction[1]//2),opponent(piece))\
                    and self.__grid[piece.row][ piece.column + (direction[1]//2)].type == PieceType.EMPTY\
                    and self.__grid[piece.row][ piece.column + (direction[1])].type == PieceType.EMPTY\
                    and (self.canCastleLeft if direction[1] < 0 else self.canCastleRigth) and self.boardState != BoardState.CHECK:
                    if direction[1] < 0:
                        if self.canCastleLeft and self.__grid[piece.row][ piece.column + (direction[1]) - 1].type == PieceType.EMPTY:
                            validMovements.append(movement)
                    else:
                        if self.canCastleLeft:
                            validMovements.append(movement)
                # Not any special cases
                elif specialCase == None:
                    validMovements.append(movement)

        return validMovements

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
        if piece.type == PieceType.EMPTY:
            return False

        # If you try to move an opponent square
        if self.is_opponent(originRow, originColumn, self.turn):
            return False

        # If the movement is an ilegal movement
        movement = (destinationRow, destinationColumn)
        playerPieces = self.whitePieces if self.turn == PlayerColor.WHITE else self.blackPieces
        if (movement not in self.get_valid_movements(piece)) if piece.type == PieceType.KING else (movement not in playerPieces[piece]):
            return False

        # If the movement leave you in check
        if self.in_check_after_mov(originRow, originColumn, destinationRow, destinationColumn):
            return False
        
        return True

    def attempt_move(self, origin_row: int, origin_column: int, destination_row: int, destination_column: int) -> tuple[bool, Optional[dict[str, Optional[Piece]]]]:
        """TODO
        """

        # Validat this movement
        if not self.is_valid_movement(origin_row,origin_column,destination_row,destination_column):
            return False, None

        eat_piece = self.__grid[destination_row][destination_column]

        # Perform movement
        piece = self.__grid[origin_row][origin_column]
        self.swap_pieces(origin_row,origin_column,destination_row,destination_column)        

        # Check for pawn special cases
        possible_en_passant = None
        if piece.type == PieceType.PAWN:
            # If move was enPassant
            if self.possibleEnPassant != None and self.possibleEnPassant[0] == destination_row and self.possibleEnPassant[1] == destination_column:
                eat_piece = self.__grid[destination_row-piece.moving_dir][destination_column]
            # If pawn performed doublemove, save it for en passant
            elif abs(destination_row-origin_row) == 2:
                possible_en_passant = (destination_row - piece.moving_dir, destination_column)
            # If pawn reached the last square it can move, promote it
            elif piece.row + piece.moving_dir == len(ROWS) or piece.row + piece.moving_dir == -1:
                self.remove_piece(piece.row, piece.column)

                if self.get_promotion_piece is None:
                    raise NotImplementedError("getPromotionPiece function not yet defined for board")

                new_piece = run(self.get_promotion_piece(piece.color, piece.row + piece.moving_dir, piece.column))
                new_piece.row = piece.row
                new_piece.column = piece.column
                self.add_piece(new_piece.row,new_piece.column, new_piece)

        elif piece.type == PieceType.KING:
            self.canCastleLeft = False
            self.canCastleRigth = False

            # If move was castle
            if abs(destination_column-origin_column) == 2:
                direction = (destination_column-origin_column)//abs(destination_column-origin_column)
                self.swap_pieces(origin_row, 0 if direction == -1 else 7, origin_row, destination_column - direction)

        self.possibleEnPassant = possible_en_passant

        # Eat opponent piece if it's eat move
        if eat_piece.type != PieceType.EMPTY:
            self.empty_square(eat_piece.row, eat_piece.column)

        # Pass turn and calculate new board conditions for next player
        self.turn = opponent(self.turn)
        self.squares_under_attack(opponent(self.turn))
        self.get_posible_turn_movements()
        self.set_game_state()

        return True, {
            'piece': piece,
            'eatPiece': eat_piece if eat_piece.type !=PieceType.EMPTY else None
        }

    def get_serialization_attrs(self) -> dict[str, Any]:
        return {
            'turn' : self.turn.value,
            'canCastleLeft' : self.canCastleLeft,
            'canCastleRigth' : self.canCastleRigth,
            'possibleEnPassant' : self.possibleEnPassant,
        }

    @classmethod
    def get_from_deserialize(cls, attrs: dict[str, Any], **kwargs: Any) -> ChessValidator:
        """TODO
        """
        board = ChessValidator(kwargs["grid"], attrs["turn"])
        board.canCastleRigth = attrs['canCastleRigth']
        board.canCastleLeft = attrs['canCastleLeft']
        board.possibleEnPassant = tuple(attrs['possibleEnPassant']) if attrs['possibleEnPassant'] != None else None
        return board