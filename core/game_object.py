# Import external libraries
from __future__ import annotations
import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):

    #! Must be called each sub class initialization
    def init_attributes(self) -> None:
        self.children: list[GameObject] = []
        self.renders = False
        self._x = 0
        self._y = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def add_child(self, index: int, obj: GameObject) -> None:
        self.children.insert(index, obj)

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: pygame.surface) -> None:
        pass
