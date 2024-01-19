"""This module handles the core user interface mechanics througth the GameManager Static class"""

import pygame
from typing import Type

# Import internal modules
from chess_engine.board import Board
from game_logic.game import Game
from game_logic.screen import Screen, ScreenBaseData
from game_logic.consts import PrintColor, PlayerColor, GameResult, ROWS, COLUMNS
from ui.font import Font

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
        
        cls.font = font
        cls.renderScreen = renderScreen
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
    def load_screen(cls, screenType: Type[Screen], **kargs):
        cls.currentScreen = screenType(ScreenBaseData(cls.font, cls.renderScreen), **kargs)

    @staticmethod
    def quit(cls):
        cls.running = False
