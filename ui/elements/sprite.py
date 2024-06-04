"""TODO"""

from dataclasses import dataclass

import pygame

from game_logic.game_object import GameObject
from utils.utils import tint_image


@dataclass
class SpriteInitData():
    """TODO
    """
    image: pygame.Surface
    centered: bool = False
    pixel_tint: bool = True
    tint: tuple[int, int, int]=(255,255,255)

class Sprite(GameObject):
    """TODO
    """

    def __init__(self, x: int, y: int, init_data: SpriteInitData):
        super().__init__()

        self._tint = (255,255,255)
        self.pixel_tint = init_data.pixel_tint
        self.original_img = init_data.image.copy()

        self.image = init_data.image
        self.rect = init_data.image.get_rect(topleft=(x,y))
        self.centered = init_data.centered

        self.x = x
        self.y = y
        self.tint = init_data.tint

    @property
    def tint(self) -> tuple[int, int, int]:
        """Tint property
        """
        return self._tint

    @tint.setter
    def tint(self, value: tuple[int, int, int]):
        if self._tint == value:
            return
        self._tint = value
        # Reset image color
        self.image = self.original_img.copy()
        tint_image(self.image, self._tint, self.pixel_tint)

    def x_setter(self, value: int) -> None:
        """X property setter
        """
        super(__class__, type(self)).x.fset(self, value) # type: ignore
        self.rect.x = self._x - (self.image.get_width()//2 if self.centered else 0)

    def y_setter(self, value: int) -> None:
        """Y propery setter
        """
        super(__class__, type(self)).y.fset(self, value) # type: ignore
        self.rect.y = self._y - (self.image.get_height()//2 if self.centered else 0)

    @property
    def x(self) -> int:
        return super().x

    @x.setter
    def x(self, value: int):
        self.x_setter(value)

    @property
    def y(self) -> int:
        return super().y

    @y.setter
    def y(self, value: int):
        self.y_setter(value)

    def update(self):
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect.topleft)
