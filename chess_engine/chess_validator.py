"""This module contains the Board model object and it's properties"""

from __future__ import annotations

from asyncio import run
from copy import deepcopy
from typing import Any, Optional, cast

from chess_engine.chess_game_data import Movement
from chess_engine.enums import MoveStatus, TurnState, ValidationStatus
from chess_engine.grid import COLUMNS, ROWS, Grid, GridIter
from chess_engine.piece import MovSpecialCase, Piece, PieceType, SideColor
from chess_engine.structs import CastlingState, Coord
from utils.exceptions import StaticClassInstanceError
from utils.utils import opponent

GridContext = tuple[SideColor, Grid]
class ChessValidator:
    """TODO
    """

    initial_piece_count = {
        PieceType.PAWN : 8,
        PieceType.BISHOP : 2,
        PieceType.KNIGTH : 2,
        PieceType.ROOK : 2,
        PieceType.QUEEN : 1,
        PieceType.KING : 1
    }

    _cached_grid_ctx: GridContext
    _cached_movements: dict[tuple[Coord, Coord], ValidationStatus] = {}

    @classmethod
    def clean_cache(cls, new_grid_ctx: GridContext) -> None:
        """TODO
        """
        cls._cached_grid_ctx = new_grid_ctx
        cls._cached_movements = {}

    @classmethod
    def _access_cache(cls, mov: tuple[Coord, Coord],
                      grid_ctx: GridContext) -> Optional[ValidationStatus]:
        if cls._cached_grid_ctx == grid_ctx:
            return cls._cached_movements[mov]
        return None

    @classmethod
    def is_valid_initial_grid(cls) -> bool:
        """TODO
        """
        grid = Grid.get_start_grid()

        white_pieces = {piece_type: 0 for piece_type in PieceType}
        for piece in grid.white_pieces:
            white_pieces[piece.type] += 1
        black_pieces = {piece_type: 0 for piece_type in PieceType}
        for piece in grid.black_pieces:
            black_pieces[piece.type] += 1

        for piece_type, ideal_count in cls.initial_piece_count.items():
            if white_pieces[piece_type] != ideal_count or black_pieces[piece_type] != ideal_count:
                return False
        return True

    @classmethod
    def is_valid_promotion_type(cls, piece_type: PieceType) -> bool:
        """TODO
        """
        return piece_type not in (PieceType.PAWN, PieceType.KING)

    @classmethod
    def is_valid_move(cls, origin: Coord, dest: Coord, last_mov: Optional[Movement],
                      castling_state: CastlingState, grid_ctx: GridContext) -> Optional[MoveStatus]:
        """TODO
        """
        validation = cls._access_cache((origin, dest), grid_ctx)
        if validation is None:
            validation = cls._is_valid_move(origin, dest, grid_ctx)
        match validation:
            case ValidationStatus.INVALID:
                return MoveStatus.INVALID
            case ValidationStatus.CHECKS_KING:
                return MoveStatus.INVALID
            case ValidationStatus.NEED_LAST_MOVE:
                context = (origin, dest, last_mov, grid_ctx)
                is_valid = cls._is_valid_enpassant(*context)
                return None if is_valid else MoveStatus.INVALID
            case ValidationStatus.NEED_CASTLING_STATE:
                context = (origin, dest, castling_state, grid_ctx)
                is_valid, new_castling = cls._is_valid_castle(*context)
                castling_state = new_castling
                return None if is_valid else MoveStatus.INVALID
            case ValidationStatus.NEED_PROMOTION_PIECE:
                return MoveStatus.REQUIRE_PROMOTION
            case _:
                return None

    @classmethod
    def _is_valid_move(cls, origin: Coord, dest: Coord, grid_ctx: GridContext) -> ValidationStatus:

        raise NotImplementedError()

    @classmethod
    def _is_valid_enpassant(cls, origin: Coord, dest: Coord, last_mov: Optional[Movement],
                           grid_ctx: GridContext) -> bool:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def _is_valid_castle(cls, origin: Coord, dest: Coord, castling_state: CastlingState,
                           grid_ctx: GridContext) -> tuple[bool, CastlingState]:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def is_pawn_promotion(cls, piece: Piece, dest: Coord, grid: Grid) -> bool:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def get_board_state(cls, last_mov: Optional[Movement], castling_state: CastlingState,
                        grid_ctx: GridContext) -> TurnState:
        """TODO
        """
        turn, grid = grid_ctx
        context = (last_mov, castling_state, grid_ctx)

        pieces = grid.white_pieces if turn == SideColor.WHITE else grid.black_pieces
        opponent_pieces = grid.white_pieces if turn == SideColor.BLACK else grid.black_pieces
        king = [p for p in pieces if p.type == PieceType.KING][0]

        any_valid_move = any(cls._has_any_valid_move(context, p) for p in pieces)
        is_in_check = any(cls._attacks_coord(p, king, grid_ctx) for p in opponent_pieces)
        if is_in_check:
            if not any_valid_move:
                return TurnState.CHECKMATE
            return TurnState.CHECK
        if not any_valid_move:
            return TurnState.STALEMATE
        return TurnState.MOVE_TURN

    @classmethod
    def _attacks_coord(cls, piece: Piece, attacked_p: Piece, grid_ctx: GridContext) -> bool:
        origin = piece.coord
        destination = attacked_p.coord
        validation = cls._is_valid_move(origin, destination, grid_ctx)
        return validation in (ValidationStatus.VALID, ValidationStatus.CHECKS_KING)

    @classmethod
    def _has_any_valid_move(cls, context: tuple[Optional[Movement], CastlingState, GridContext],
                            piece: Piece) -> bool:
        for possible_mov in piece.movements:
            origin = piece.coord
            destination = Coord(origin.row-possible_mov.y, origin.column+possible_mov.x)
            invalid = cls.is_valid_move(origin, destination, *context)
            if invalid not in (None, MoveStatus.REQUIRE_PROMOTION):
                return False
        return True

    def is_opponent(self, row: int, column: int, playerColor: SideColor) -> bool:
        """Returns whether the square is ocuppied by an opponent piece or not

        Args:
            row (int): Row.
            column (int): Column.
            playerColor(PlayerColor): The player color.

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].color == opponent(playerColor)

    def is_player(self, row: int, column: int, playerColor: SideColor) -> bool:
        """Returns whether the square is ocuppied by a piece of the player or not

        Args:
            row (int): Row
            column (int): Column
            playerColor(PlayerColor): The player which is checking for it's color

        Returns:
            bool: Ocuppied or not
        """
        
        return self.__grid[row][column].color == playerColor

    def is_attacked(self, row: int, column: int, opponent: SideColor) -> bool:
        """Determines if the specified square is attacked by the opponent or not

        Args:
            row (int): Square row.
            column (int): Square column.
            opponent (PlayerColor): Opponent that is attacking.

        Returns:
            bool: Whether the square is attacked or not
        """
        
        opponentPieces = self.whitePieces if opponent == SideColor.WHITE else self.blackPieces
        return any((row,column) in attackedSquares for attackedSquares in opponentPieces.values())

    def squares_under_attack(self, opponent: SideColor) -> None:
        """Calculate the squares under attack by the opponent pieces

        Args:
            opponent (PlayerColor): Opponent color.
        """

        opponentPieces = self.whitePieces if opponent == SideColor.WHITE else self.blackPieces
        
        for piece, posibleMovs in opponentPieces.items():
            posibleMovs.clear()
            for movement in self.get_valid_movements(piece, True):
                if piece.type != PieceType.PAWN:
                    posibleMovs.append(movement)
                elif piece.column != movement[1]: # If the movement is different to pawn frontal move, add it
                    posibleMovs.append(movement)

    def get_posible_turn_movements(self, turn: SideColor = None) -> None:
        """Calculate the squares which the turn pieces can move to

        Args:
            turn (PlayerColor, optional): Player turn. Defaults to None.
        """
        
        if turn == None:
            turn = self.turn
        
        playerPieces = self.whitePieces if turn == SideColor.WHITE else self.blackPieces
        
        for piece, posibleMovs in playerPieces.items():
            posibleMovs.clear()
            posibleMovs += self.get_valid_movements(piece)

    def set_game_state(self, afterMoveCheck: bool = False) -> None:
        """Evaluates if the board state of the player whoose turn is next
        
        Args:
            afterMoveCheck (bool, optional): Whether to not determine if the current board is checkmate or stalemate, used for avoiding infinite recursion loops. Defaults to false.
        """
        
        playerKing = self.whiteKing if self.turn == SideColor.WHITE else self.blackKing
        inCheck = self.is_attacked(playerKing.row, playerKing.column, opponent(self.turn))
        
        # Check whether to continuo with stalemate or checkmate validation
        if afterMoveCheck:
            self.boardState = TurnState.CHECK if inCheck else TurnState.MOVE_TURN
            return
        
        # If only kings left in board, mark stalemate
        if len(self.whitePieces) == 1 and len(self.blackPieces == 1):
            self.boardState = TurnState.STALEMATE
            return

        # Validate if the player has any legal movement available, if not it's either stalemate or checkmate
        anyValidMov = False
        playerPieces = self.whitePieces if self.turn == SideColor.WHITE else self.blackPieces
        for piece, posibleMovs in playerPieces.items():
            if any((not self.in_check_after_mov(piece.row, piece.column, mov[0], mov[1])) for mov in posibleMovs):
                anyValidMov = True
                break
                
        # Set board state
        if not anyValidMov and inCheck:
            self.boardState = TurnState.CHECKMATE
        elif inCheck:
            self.boardState = TurnState.CHECK
        elif not anyValidMov:
            self.boardState = TurnState.STALEMATE
        else:
            self.boardState = TurnState.MOVE_TURN

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

        return hipothetycalBoard.boardState == TurnState.CHECK or hipothetycalBoard.boardState == TurnState.CHECKMATE

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
                        ((piece.row == 1 and piece.color == SideColor.BLACK) or (piece.row == 6 and piece.color == SideColor.WHITE))\
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
                    and (self.canCastleLeft if direction[1] < 0 else self.canCastleRigth) and self.boardState != TurnState.CHECK:
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
        playerPieces = self.whitePieces if self.turn == SideColor.WHITE else self.blackPieces
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

    def __init__(self) -> None:
        raise StaticClassInstanceError(ChessValidator)
