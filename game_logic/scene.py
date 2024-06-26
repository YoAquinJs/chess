"""TODO"""

from abc import ABC

import pygame

from game_logic.game_object import GameObject


class Scene(ABC):
    """TODO
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.game_objects: list[GameObject] = []

    def register_obj(self, obj: GameObject) -> None:
        """Registers a GameObject to the scene

        Args:
            obj (GameObject): GameObject

        Raises:
            Exception: When object already registered to the scene
        """
        if obj in self.game_objects:
            raise ValueError("Object already added to scene")

        self.game_objects.append(obj)
        for child in obj.children:
            self.register_obj(child)

    def update(self) -> None:
        """Update objects
        """
        for obj in self.game_objects:
            obj.update()

    def render(self) -> None:
        """Render objects
        """
        for obj in self.game_objects:
            obj.render(self.screen)
