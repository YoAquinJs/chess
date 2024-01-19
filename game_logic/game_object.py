# Import external libraries
from __future__ import annotations
import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):

    #! Must be called each sub class initialization
    def init_attributes(self) -> None:
        self.children: list[GameObject] = []
        if not hasattr(self, '_x'):
            self._x: int = 0
        if not hasattr(self, '_y'):
            self._y: int = 0
        if not hasattr(self, 'drag_children'):
            self.drag_children: bool = False

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        if self.drag_children:
            delta = value - self._x
            for child in self.children:
                child.x += delta
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        if self.drag_children:
            delta = value - self._y
            for child in self.children:
                child.y += delta
        self._y = value

    def add_child(self, index: int, obj: GameObject) -> None:
        self.children.insert(index, obj)

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass
