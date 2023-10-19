"""This module handles the core user interface mechanics througth the GameManager Static class"""

# Import internal modules
from utils.utils import color_print
from core.game import Game
from chess_engine.board import Board
from core.consts import GameScreen, InputType, PrintColor, PlayerColor, GameResult, ROWS, COLUMNS

class GameManager():
    """Class for handling game screens, and game states

    Attributes:
        currentScreen (GameScreen): Screen being rendered in the game.
        currentGame (Game): Current game.
        
    """

    currentScreen: GameScreen = None
    currentGame: Game = None
    loadedGame: int = -1
    
    @classmethod
    def init_game(cls):
        """Initializes the game
        """
        
        print("-------------C H E S S-------------")
        print("Start new Game or load existing game")
        
        cls.currentScreen = GameScreen.mainMenu
        
    @classmethod
    def update(cls):
        """User console interface logic

        Raises:
            ValueError: When unvalid inputs.
        """

        try:
            if cls.currentScreen == GameScreen.mainMenu:
                loadGame = GameManager.user_input("Select game option (New game(0)/Load(1)): ", InputType.bool)
                if loadGame:
                    games = Game.get_saved_games(True)

                    if len(games) == 0:
                        print("No games saved")
                        return

                    for i, game in enumerate(games, 1):
                        color_print(f"{i}. {game.gameResult.value}", PrintColor.blue)
                        printHistory = GameManager.user_input("Print history ((No(0)/Yes(1)): ", InputType.bool)
                        if printHistory:
                            if len(game.moveHistory) > 0:
                                game.print_history()
                            else:
                                print("No movements")

                    cls.load_game()
                else:
                    cls.start_new_game()
            
            elif cls.currentScreen == GameScreen.onGame:
                cls.render_board()
                color_print(f"Turn: {'White' if cls.currentGame.board.turn == PlayerColor.white else 'Black'} Status: {cls.currentGame.board.boardState.value}", PrintColor.blue)

                move = GameManager.user_input("Select game option (Exit(0)/Move(1)): ", InputType.bool)

                if move:
                    if cls.currentGame.gameResult != GameResult.pending:
                        print("Game not pending")
                        return
                    
                    cls.call_movement()
                else:
                    save = GameManager.user_input("Select game option (Exit(0)/Save(1)): ", InputType.bool)
                    if save:
                        cls.save_game()
                    else:
                        print("Exit game")
                        cls.currentGame = None
                        cls.currentScreen = GameScreen.mainMenu                    
        except ValueError:
            pass
        
    @classmethod
    def save_game(cls):
        """Saves the current game if possible
        """
        
        gameIdx = len(Game.get_saved_games())+1 if cls.loadedGame == -1 else cls.loadedGame
        serialized, status = cls.currentGame.serialize(str(gameIdx))
        if not serialized:
            color_print(f"Couldn't save, reason: {status}\nReturn to game", PrintColor.red)
        else:
            color_print("Succesfully saved", PrintColor.blue)
            cls.currentGame = None
            cls.currentScreen = GameScreen.mainMenu
    
    @classmethod
    def load_game(cls):
        selection = GameManager.user_input("Select game by index (Number): ", InputType.int)
        if selection < 1 or selection > len(Game.get_saved_games()):
            raise ValueError()
        
        cls.currentGame = Game.deserialize(str(selection))
        if cls.currentGame != None:
            color_print(f"Loaded game {selection}", PrintColor.blue)
            cls.currentScreen = GameScreen.onGame
            cls.loadedGame = selection
        else:
            color_print(f"Couldn't load game {selection}", PrintColor.red)
  
    @classmethod
    def start_new_game(cls):
        cls.currentGame = Game.new_game()
        cls.currentScreen = GameScreen.onGame
        cls.loadedGame = -1
    
    @classmethod
    def call_movement(cls):
        originRow = GameManager.user_input("Input origin row (Number): ", InputType.str).replace(" ","")
        originColumn = GameManager.user_input("Input origin column (Letter): ", InputType.str).replace(" ","")
        destinationRow = GameManager.user_input("Input destination row (Number): ", InputType.str).replace(" ","")
        destinationColumn = GameManager.user_input("Input destination column (Letter): ", InputType.str).replace(" ","")
        
        try:
            originRow = ROWS.index(originRow)
            originColumn = COLUMNS.index(originColumn)
            destinationRow = ROWS.index(destinationRow)
            destinationColumn = COLUMNS.index(destinationColumn)

            if not cls.currentGame.user_move((originRow,originColumn,destinationRow,destinationColumn)):
                color_print("Invalid Movement", PrintColor.red)
        except:
            color_print("Invalid Input", PrintColor.red)

    
    @classmethod
    def render_board(cls):
        if cls.currentGame is not None:
            cls.currentGame.board.print_board()

    @staticmethod
    def user_input(input_text: str, input_type: InputType) -> object:
        """Gets user console input

        Args:
            input_text (str): Input prompt text.
            input_type (InputType): Input return type

        Raises:
            ValueError: When parse is incorrect

        Returns:
            object: Input parsed.
        """
        
        color_print(input_text, PrintColor.green)
        ipt = input()

        try:
            if input_type == InputType.bool:
                if ipt == '0':
                    return False
                if ipt == '1':
                    return True
                else:
                    raise ValueError()
            elif input_type == InputType.int:
                return int(ipt)
            elif input_type is InputType.str:
                return ipt
        except:
            color_print("Incorrect input", PrintColor.red)
            raise ValueError()
            
    #//@classmethod
    #//def render(cls):
    #//    pass        
    #//
    #//@classmethod
    #//def render_ui(cls):
    #//    pass
