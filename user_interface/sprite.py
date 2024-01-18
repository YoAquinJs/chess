import pygame

from utils.utils import tint_image
from core.game_object import GameObject

class Sprite(GameObject):
    def __init__(self, x: int, y: int, image: pygame.Surface, centered=False,
                 color: tuple[int, int, int]=None, tint: tuple[int, int, int]=(255,255,255)):
        self.init_attributes()
        
        if color is None:
            color = image.get_at((0,0))
        
        self._tint = (255,255,255)
        self._color = color
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))
        self.centered = centered
        
        self.x = x
        self.y = y
        self.tint = tint

    @property
    def tint(self):
        return self._tint

    @tint.setter
    def tint(self, value):
        if self._tint == value:
            return
        self._tint = value
        self.image.fill(self._color)
        tint_image(self.image, self._tint)

    @GameObject.x.setter
    def x(self, value):
        if value < 0:
            raise ValueError("GameObject's x coordinate must not be negative")
        
        self._x = value
        self.rect.x = self._x - (self.image.get_width()//2 if self.centered else 0)
        #print(value, newRectX, self.image.get_rect())

    @GameObject.y.setter
    def y(self, value):
        if value < 0:
            raise ValueError("GameObject's y coordinate must not be negative")
        
        self._y = value
        self.rect.y = self._y - (self.image.get_height()//2 if self.centered else 0)

    def update(self):
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect.topleft)
