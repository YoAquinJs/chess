"""TODO"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """TODO
    """
    def __init__(self) -> None:
        self.children: list[GameObject] = []
        if not hasattr(self, '_x'):
            self._x: int = 0
        if not hasattr(self, '_y'):
            self._y: int = 0
        if not hasattr(self, 'drag_children'):
            self.drag_children: bool = False

    @property
    def x(self) -> int:
        """X position property
        """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if self.drag_children:
            self._drag_children_x(value)
        self._x = value

    @property
    def y(self) -> int:
        """Y postion property
        """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if self.drag_children:
            self._drag_children_y(value)
        self._y = value

    def _drag_children_x(self, value: int) -> None:
        delta = value - self.x
        for child in self.children:
            child.x += delta

    def _drag_children_y(self, value: int) -> None:
        delta = value - self.y
        for child in self.children:
            child.y += delta

    def add_child(self, index: int, obj: GameObject) -> None:
        """Adds a children GameObject
        """
        self.children.insert(index, obj)

    @abstractmethod
    def update(self) -> None:
        """Update
        """

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render
        """
