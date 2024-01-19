import pygame
from abc import ABC
from dataclasses import dataclass

from game_logic.game_object import GameObject
from ui.font import Font

@dataclass
class SceneBaseData:
    font: Font
    screen: pygame.Surface

class Scene(ABC):

    def __init__(self, baseData: SceneBaseData) -> None:
        self.font = baseData.font
        self.screen = baseData.screen
        self.gameObjects: list[GameObject] = []

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
            obj.render(self.screen)
