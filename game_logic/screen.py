import pygame
from abc import ABC, abstractmethod

from game_logic.game_object import GameObject
from ui.font import Font

class Screen(ABC):

    def __init__(self, renderScreen: pygame.Surface, font: Font) -> None:
        self.renderScreen = renderScreen
        self.font = font
        self.gameObjects: list[GameObject] = []
        self.init_objects()

    @abstractmethod
    def init_objects(self) -> None:
        pass

    def register_obj(self, obj: GameObject) -> None:
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
            obj.render(self.renderScreen)
