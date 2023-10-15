from consts import OnGameState, GameScreen, PlayerColor
from board import Board

#TODO all
class GameManager():
    """Class for handling game screens, and game states

    Attributes:
        onGameState (OnGameState): State of a game of chess
        gameScreen (GameScreen): Screen being rendered in the game
        currentPlayer (PlayerColor): 
        currentBoard (Board): State of a game of chess
        
    """

    def __init__(self) -> None:
        self.onGameState: OnGameState = None
        self.gameScreen: GameScreen = None
        self.currentPlayer: PlayerColor = None
        self.currentBoard: Board = None