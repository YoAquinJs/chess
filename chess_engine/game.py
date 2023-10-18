"""This module contains the model class game for handling Gameplay functionalities"""


from json import dumps, load
from typing import List, Union

from board import Board
from core.consts import BoardState, GameScreen, GameResult, PlayerColor, SAVINGS

#TODO all
class Game():
    """Class for handling game functionalities

    Attributes:
        gameResult (GameResult): Game result status.
        board (Board): Board of the game.
        moveHistory (List[Union, optional): Move istory of the game. Defaults to [].
        
    """

    def __init__(self, gameResult: GameResult, board: Board, moveHistory: List[Union(int, int)] = []):
        """Creates a Game object

        Args:
            gameResult (GameResult): Game result status.
            board (Board): Board of the game.
            moveHistory (List[Union, optional): Move istory of the game. Defaults to [].
        """
        
        self.gameResult = gameResult
        self.board = board
        self.moveHistory = moveHistory
        
        self.board.getPromotionPiece = self.getPromotionPiece
        self.gameState = self.board.boardState
        
    #TODO
    async def getPromotionPiece(self):
        pass
    
    def user_move(self, movement: Union[int,int,int,int]):
        """Attempts a move and record it if it was succesfull

        Args:
            movement (Union[int,int,int,int]): Movement to be attempted
        """
        
        if self.gameResult != GameResult.pending:
            return
        
        if not self.board.attempt_move(movement[0], movement[1], movement[2], movement[3]):
            return #TODO provide feddback if invalid move
        
        self.moveHistory.append(movement)
        
        if self.board.boardState == BoardState.checkmate:
            self.gameResult = GameResult.whiteWin if self.board.turn == PlayerColor.black else GameResult.blackWin  
        elif self.board.boardState == BoardState.stalemate:
            self.gameResult == GameResult.stalemate
        
        #TODO provide feedback if valid move
    
    def serialize(self, filename: str) -> bool:
        """Serializes the game to a json file

        Args:
            filename (str): The name of the json file.

        Returns:
            bool: Whether the serialization process was succesfull or not.
        """
        
        try:
            with open(f"{SAVINGS}{filename}_game.json", "w") as file:
                data = {
                    'gameResult' : self.gameResult,
                    'moveHistory' : self.moveHistory,
                    }
                
                file.write(dumps(data, indent=4))
            return True
        except Exception as e:
            print(e)
            return False    

    @classmethod
    def deserialize(cls, filename: str) -> object:
        """Deserializes from a json to a Game object
        
        Args:
            filename (str): The name of the json file.

        Returns:
            Board: Deserialized instance of Game object, or None if failed to deserialize
        """
        
        board = None
        with open(f"{SAVINGS}{filename}_game.json", "r") as file:
            json_data = load(file)
            
            board = Board.deserialize(filename)
            if board == None:
                raise Exception(f"Coulnd't deserialize board {filename}, therefore can't load Game\nFull Path: {SAVINGS}{filename}_board.json")
        
            game = cls(json_data["gameResult"], board, PlayerColor[json_data['moveHistory']])

        return game
