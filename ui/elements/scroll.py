"""TODO"""

from dataclasses import dataclass

from game_logic.game_object import GameObject
from ui.elements.sprite import Sprite


@dataclass
class ScrollInitData():
    """TODO
    """
    max_scroll: int
    background_img: Sprite
    handle: Sprite

class Scroll(GameObject):
    """Scroll gameobject
    """

    def __init__(self, x: int, y: int, init_data: ScrollInitData) -> None:
        super().__init__()
        self.drag_children = True

        self.width = init_data.background_img.image.get_width()
        self.heigth = init_data.background_img.image.get_height()

        if init_data.handle.image.get_width() != self.width:
            raise ValueError("The handle and background must have the same width")

        self.handle_heigth: int
        self._max_scroll = 0
        self.max_scroll = init_data.max_scroll
        self.x = x
        self.y = y

    @property
    def max_scroll(self) -> int:
        """TODO
        """
        return self._max_scroll

    @max_scroll.setter
    def max_scroll(self, value: int):
        self._max_scroll = value

    #def set_handle_heigth(self) -> int:
    #    """TODO
    #    """
    #    self.handle_heigth = pygame.math.clamp(self.width/self.max_scroll, 0, 1)*self.max_scroll
