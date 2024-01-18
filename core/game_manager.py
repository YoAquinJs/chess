"""This module handles the core user interface mechanics througth the GameManager Static class"""

import pygame
from typing import Type

# Import internal modules
from chess_engine.board import Board
from core.game import Game
from core.screen import Screen;
from core.consts import PrintColor, PlayerColor, GameResult, ROWS, COLUMNS
from user_interface.font import Font

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
    def init_game(cls, renderScreen: pygame.Surface, font: Font, intialScreen: Type[Screen]):
        """Initializes the game
        """
        
        cls.renderScreen = renderScreen
        cls.font = font
        cls.load_screen(intialScreen)

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
    def load_screen(cls, screenType: Type[Screen]):
        cls.currentScreen = screenType(cls.renderScreen, cls.font)

    @staticmethod
    def quit(cls):
        cls.running = False
