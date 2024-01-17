"""This module handles the core user interface mechanics througth the GameManager Static class"""

import pygame

# Import internal modules
from utils.utils import color_print
from chess_engine.board import Board
from core.game import Game
from core.screen import Screen;
from core.consts import GameScreen, PrintColor, PlayerColor, GameResult, ROWS, COLUMNS
from user_interface.font import Font

from screens.game import GameScreen
from screens.main_menu import MainMenuScreen
from screens.load_game import LoadGameScreen

class GameManager():
    """Class for handling game screens, and game states

    Attributes:
        currentScreen (GameScreen): Screen being rendered in the game.
        currentGame (Game): Current game.
    """

    renderScreen: pygame.Surface = None
    font: Font = None
    running = True

    currentScreen: Screen = None
    currentGame: Game = None
    loadedGame: int = -1

    @classmethod
    def init_game(cls, renderScreen: pygame.Surface, font: Font):
        """Initializes the game
        """
        
        cls.renderScreen = renderScreen
        cls.font = font
        cls.currentScreen = MainMenuScreen(cls.renderScreen, cls.font)

    @classmethod
    def update(cls):
        """Runs the logic of the game based on the loaded screen
        """
        
        cls.currentScreen.update()

        #try:
        #    if cls.currentScreen == GameScreen.mainMenu:
        #        loadGame = GameManager.user_input("Select game option (New game(0)/Load(1)): ", InputType.bool)
        #        if loadGame:
        #            games = Game.get_saved_games(True)
        #
        #            if len(games) == 0:
        #                print("No games saved")
        #                return
        #
        #            for i, game in enumerate(games, 1):
        #                color_print(f"{i}. {game.gameResult.value}", PrintColor.blue)
        #                printHistory = GameManager.user_input("Print history ((No(0)/Yes(1)): ", InputType.bool)
        #                if printHistory:
        #                    if len(game.moveHistory) > 0:
        #                        game.print_history()
        #                    else:
        #                        print("No movements")
        #
        #            cls.load_game()
        #        else:
        #            cls.start_new_game()
        #    
        #    elif cls.currentScreen == GameScreen.onGame:
        #        cls.render_board()
        #        color_print(f"Turn: {'White' if cls.currentGame.board.turn == PlayerColor.white else 'Black'} Status: {cls.currentGame.board.boardState.value}", PrintColor.blue)
        #
        #        move = GameManager.user_input("Select game option (Exit(0)/Move(1)): ", InputType.bool)
        #
        #        if move:
        #            if cls.currentGame.gameResult != GameResult.pending:
        #                print("Game not pending")
        #                return
        #            
        #            cls.call_movement()
        #        else:
        #            save = GameManager.user_input("Select game option (Exit(0)/Save(1)): ", InputType.bool)
        #            if save:
        #                cls.save_game()
        #            else:
        #                print("Exit game")
        #                cls.currentGame = None
        #                cls.currentScreen = GameScreen.mainMenu                    
        #except ValueError:
        #    pass

    @classmethod
    def render(cls):
        """Runs the rendering of the game based on the loaded screen
        """
        
        cls.currentScreen.render()


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
    def start_new_game(cls):
        cls.currentGame = Game.new_game()
        cls.currentScreen = GameScreen.onGame
        cls.loadedGame = -1

    @classmethod
    def render_board(cls):
        if cls.currentGame is not None:
            cls.currentGame.board.print_board()

    @staticmethod
    def quit(cls):
        cls.running = False
