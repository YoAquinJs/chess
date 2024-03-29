"""TODO"""

from typing import Any, Type

import pygame

# Import internal modules
from chess_engine.chess_game import ChessGame
from ui.scene import Scene, SceneBaseData
from ui.font import Font
from utils.exceptions import StaticClassInstanceError


class GameManager():
    """TODO
    """
    screen: pygame.Surface
    font: Font
    running = True

    currentScene: Scene
    currentGame: ChessGame
    loadedGame: int = -1

    @classmethod
    def init_game(cls, screen: pygame.Surface, font: Font, intial_scene: Type[Scene]) -> None:
        """Initializes the game
        """
        cls.font = font
        cls.screen = screen
        cls.load_screen(intial_scene)

    @classmethod
    def update(cls) -> None:
        """Runs the logic of the game based on the loaded screen
        """
        cls.currentScene.update()

    @classmethod
    def render(cls) -> None:
        """Runs the rendering of the game based on the loaded screen
        """
        cls.currentScene.render()

    @classmethod
    def load_screen(cls, scene_type: Type[Scene], **kwargs: Any) -> None:
        """Loads the specified scene
        """
        cls.currentScene = scene_type(SceneBaseData(cls.font, cls.screen), **kwargs)

    @classmethod
    def quit(cls) -> None:
        """Get's out of the game loop
        """
        cls.running = False

    def __init__(self) -> None:
        raise StaticClassInstanceError(GameManager)
