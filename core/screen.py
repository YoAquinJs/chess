import pygame
from abc import ABC, abstractmethod

from core.game_object import GameObject
from user_interface.font import Font

class Screen(ABC):

    def __init__(self, renderScreen: pygame.Surface, font: Font) -> None:
        self.renderScreen = renderScreen
        self.font = font
        self.gameObjects: list[GameObject] = []
        self.init_objects()

    @abstractmethod
    def init_objects(self):
        pass

    def register_obj(self, obj: GameObject):
        if obj in self.gameObjects:
            raise Exception("Object already added to scene")

        self.gameObjects.append(obj)
        for child in obj.children:
            self.register_obj(child)

    def update(self) -> None:
        for obj in self.gameObjects:
            obj.update()

    def render(self) -> None:
        for obj in self.gameObjects:
            if not obj.renders:
                continue
            obj.render(self.renderScreen)
