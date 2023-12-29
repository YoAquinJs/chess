# Import external libraries
from __future__ import annotations
import pygame

class GameObject:

    def __init__(self, x: int, y: int, image: pygame.image) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.children = []

    def add_child(self, obj: GameObject):
        self.children.append(obj)

    def update(self):
        pass

    def render(self, surface: pygame.surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
