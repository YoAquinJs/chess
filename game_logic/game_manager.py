"""This module handles the core user interface mechanics througth the GameManager Static class"""

import pygame
from typing import Type

# Import internal modules
from chess_engine.board import Board
from game_logic.game import Game
from game_logic.scene import Scene, SceneBaseData
from game_logic.consts import PrintColor, PlayerColor, GameResult, ROWS, COLUMNS
from ui.font import Font

class GameManager():
    """Class for handling game screens, and game states

    Attributes:
        currentScreen (Screen): Screen being rendered in the game.
        currentGame (Game): Current game.
    """

    screen: pygame.Surface = None
    font: Font = None
    running = True

    currentScene: Scene = None
    currentGame: Game = None
    loadedGame: int = -1

    @classmethod
    def init_game(cls, renderScreen: pygame.Surface, font: Font, intialScene: Type[Scene]):
        """Initializes the game
        """
        
        cls.font = font
        cls.screen = renderScreen
        cls.load_screen(intialScene)

    @classmethod
    def update(cls):
        """Runs the logic of the game based on the loaded screen
        """
        
        cls.currentScene.update()

    @classmethod
    def render(cls):
        """Runs the rendering of the game based on the loaded screen
        """
        
        cls.currentScene.render()

    @classmethod
    def load_screen(cls, sceneType: Type[Scene], **kargs):
        cls.currentScene = sceneType(SceneBaseData(cls.font, cls.screen), **kargs)

    @staticmethod
    def quit(cls):
        cls.running = False
