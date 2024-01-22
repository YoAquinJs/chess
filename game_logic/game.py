"""This module contains the model class game for handling Gameplay functionalities"""

# Import external libraries
from json import dump, load
from os import listdir, path
from typing import List, Union

# Import Internal modules
from chess_engine.board import Board
from chess_engine.piece import Piece
from game_logic.consts import (COLUMNS, MAX_GAMES_SAVED, ROWS, AssetType,
                               BoardState, GameResult, PieceType, PlayerColor)
from utils.utils import get_asset_path


class Game():
    """Class for handling game functionalities

    Attributes:
        gameResult (GameResult): Game result status.
        board (Board): Board of the game.
        moveHistory (List[Union(str, str, Union(int, int), optional): Move istory of the game. Defaults to [].
    """

    fileEnd = '_g.json'

    def __init__(self, gameResult: GameResult, board: Board, moveHistory: List[Union[str, str, Union[int, int]]] = []):
        """Creates a Game object

        Args:
            gameResult (GameResult): Game result status.
            board (Board): Board of the game.
            moveHistory (List[str, str, Union[int, int]], optional): Move istory of the game. Defaults to [].
        """
        
        self.gameResult = gameResult
        self.board = board
        self.moveHistory = moveHistory
        
        self.board.getPromotionPiece = self.getPromotionPiece

    async def getPromotionPiece(self, color: PlayerColor, row: int, column: int) -> Piece:
        """Asks the user for the promotion piece

        Args:
            color (PlayerColor): Piece color.
            row (int): Piece instantiation row.
            column (int): Piece instantiation column.

        Returns:
            Piece: Promotion Piece
        """
        
        pieceType = None
        while pieceType == None:
            try:
                pieceType = PieceType[input("Enter the promotion piece: ")]
                if pieceType == PieceType.KING:
                    pieceType = None
            except:
                pass
            
        return Piece(pieceType, color, row, column)

    def user_move(self, movement: Union[int,int,int,int]) -> bool:
        """Attempts a move and record it if it was succesfull

        Args:
            movement (Union[int,int,int,int]): Movement to be attempted
            
        Returns:
            bool: Whether the movemernt was performed or not
        """
        
        if self.gameResult != GameResult.PENDING:
            return
        
        moved, moveInf = self.board.attempt_move(movement[0], movement[1], movement[2], movement[3])
        if not moved:
            return False
        
        self.moveHistory.append((str(moveInf["piece"]), None if moveInf["eatPiece"] == None else str(moveInf["eatPiece"]), movement))
        
        if self.board.boardState == BoardState.CHECKMATE:
            self.gameResult = GameResult.WHITE_WIN if self.board.turn == PlayerColor.BLACK else GameResult.BLACK_WIN  
        elif self.board.boardState == BoardState.STALEMATE:
            self.gameResult == GameResult.STALEMATE
        
        return True

    def serialize(self, filename: str) -> Union[bool, str]:
        """Serializes the game to a json file

        Args:
            filename (str): The name of the json file.

        Returns:
            bool: Whether the game was serialized or not.
            str: Operation status of the serialization process, succesfull, failed or max games saved reached.
        """
        
        if len(Game.get_saved_games()) >= MAX_GAMES_SAVED:
            return False, "Max games saved reached"
        
        try:
            with open(get_asset_path(AssetType.SAVINGS, f"game_{filename}{Game.fileEnd}"), "w") as file:
                if not self.board.serialize(filename):
                    raise Exception("Couldn't serialize board")
                
                data = {
                    'gameResult' : self.gameResult.value,
                    'moveHistory' : self.moveHistory
                    }
                
                dump(data, file)
            return True, "Succesfull"
        except Exception as e:
            print(e)
            return False, "Failed"    

    def print_history(self) -> None:
        """Print the move history of this game
        """
        
        for mov in self.moveHistory:
            print(f"{mov[0]}{f' Capture {mov[1]}' if mov[1] != None else ''} - ({ROWS[mov[2][0]]},{COLUMNS[mov[2][1]]}) to ({ROWS[mov[2][2]]},{COLUMNS[mov[2][3]]})")

    @classmethod
    def deserialize(cls, filename: str) -> object:
        """Deserializes from a json to a Game object
        
        Args:
            filename (str): The name of the json file.

        Returns:
            Board: Deserialized instance of Game object, or None if failed to deserialize
        """
        
        board = None
        with open(get_asset_path(AssetType.SAVINGS, f"game_{filename}{Game.fileEnd}"), "r") as file:
            json_data = load(file)
            
            board = Board.deserialize(filename)
            if board == None:
                boardPath = get_asset_path(AssetType.SAVINGS, f"board_{filename}{Board.fileEnd}")
                raise Exception(f"Coulnd't deserialize board {filename}, therefore can't load Game\nFull Path: {boardPath}")
        
            # Parse the json data the Game object
            game = cls(GameResult[json_data["gameResult"]], board, [(mov[0], mov[1], (mov[2][0],mov[2][1],mov[2][2],mov[2][3])) for mov in json_data['moveHistory']])

        return game

    @staticmethod
    def get_saved_games(serialized: bool = False) -> List[str] | List[object]:
        """Returns the list of names for all the games saved

        Args:
            serialized (bool, optional): Whether to return the games serialized or not. Defaults to False.

        Returns:
            List[str]: List of saved games.
        """
        
        filenameList = [f[len("game_"):-len(Game.fileEnd)] for f in listdir(AssetType.SAVINGS.value) if path.isfile(get_asset_path(AssetType.SAVINGS.value, f)) and f.endswith(Game.fileEnd)]
        if not serialized:
            return filenameList
        else:
            return [Game.deserialize(f) for f in filenameList]

    @classmethod
    def new_game(cls) -> object:
        """Returns a Game object with all parameters to default

        Returns:
            object: Game object
        """
        
        board = Board.start_board()
        return cls(GameResult.PENDING, board,)
