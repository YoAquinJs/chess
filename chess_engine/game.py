"""This module contains the model class game for handling Gameplay functionalities"""

from os import listdir, path
from json import dumps, load
from typing import List, Union

from board import Board
from core.consts import BoardState, GameScreen, GameResult, PlayerColor, SAVINGS, MAX_GAMES_SAVED

#TODO all
class Game():
    """Class for handling game functionalities

    Attributes:
        gameResult (GameResult): Game result status.
        board (Board): Board of the game.
        moveHistory (List[Union(str, str, Union(int, int), optional): Move istory of the game. Defaults to [].
        
    """

    def __init__(self, gameResult: GameResult, board: Board, moveHistory: List[Union(str, str, Union(int, int))] = []):
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
        
        moved, moveInf = self.board.attempt_move(movement[0], movement[1], movement[2], movement[3])
        if not moved:
            return #TODO provide feddback if invalid move
        
        self.moveHistory.append((str(moveInf["piece"]), None if moveInf["eatPiece"] == None else str(moveInf["eatPiece"]), movement))
        
        if self.board.boardState == BoardState.checkmate:
            self.gameResult = GameResult.whiteWin if self.board.turn == PlayerColor.black else GameResult.blackWin  
        elif self.board.boardState == BoardState.stalemate:
            self.gameResult == GameResult.stalemate
        
        #TODO provide feedback if valid move
    
    def serialize(self, filename: str) -> str:
        """Serializes the game to a json file

        Args:
            filename (str): The name of the json file.

        Returns:
            str: Operation status of the serialization process, succesfull, failed or max games saved reached.
        """
        
        if len(Game.get_saved_games()) >= MAX_GAMES_SAVED:
            return "Max games saved reached"
        
        try:
            with open(f"{SAVINGS}{filename}_game.json", "w") as file:
                data = {
                    'gameResult' : self.gameResult,
                    'moveHistory' : self.moveHistory,
                    }
                
                file.write(dumps(data, indent=4))
            return "Succesfull"
        except Exception as e:
            print(e)
            return "Failed"    

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
        
            # Parse the json data the Game object
            game = cls(json_data["gameResult"], board, [(mov[0], mov[1], (mov[2][0],mov[2][1])) for mov in json_data['moveHistory']])

        return game

    @staticmethod
    def get_saved_games() -> List[str]:
        """Returns the list of names for all the games saved

        Returns:
            List[str]: List of saved games.
        """
        
        filend = '_game.json'
        return [f[:-len(filend)] for f in listdir(SAVINGS) if path.isfile(path.join(SAVINGS, f)) and f.endswith(filend)]
    
    @classmethod
    def new_game(cls) -> object:
        """Returns a Game object with all parameters to default

        Returns:
            object: Game object
        """
        board = Board.start_board()
        return cls(GameResult.pending, board,)
