"""This module handles the core user interface mechanics througth the GameManager Static class"""

import pygame

# Import internal modules
from utils.utils import color_print
from chess_engine.board import Board
from core.game import Game
from core.screen import Screen;
from core.consts import GameScreenType, PrintColor, PlayerColor, GameResult, ROWS, COLUMNS
from user_interface.font import Font

from screens.on_game import OnGameScreen
from screens.main_menu import MainMenuScreen
from screens.load_game import LoadGameScreen

class GameManager():
    """Class for handling game screens, and game states

    Attributes:
        currentScreen (Screen): Screen being rendered in the game.
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
        cls.load_screen(GameScreenType.mainMenu)

    @classmethod
    def update(cls):
        """Runs the logic of the game based on the loaded screen
        """
        
        cls.currentScreen.update()

    @classmethod
    def render(cls):
        """Runs the rendering of the game based on the loaded screen
        """
        
        cls.currentScreen.render()

    @classmethod
    def load_screen(cls, type: GameScreenType):
        if type == GameScreenType.mainMenu:
            cls.currentScreen = MainMenuScreen(cls.renderScreen, cls.font)
        elif type == GameScreenType.onGame:
            cls.currentScreen = OnGameScreen(cls.renderScreen, cls.font)
        elif type == GameScreenType.loadGame:
            cls.currentScreen = LoadGameScreen(cls.renderScreen, cls.font)

    @staticmethod
    def quit(cls):
        cls.running = False
