"""TODO"""

from dataclasses import dataclass, field

import pygame


@dataclass
class Text():
    """Class container for text rendering
    """
    value: str
    scale: float = 1
    character_imgs: list[pygame.Surface] = field(default_factory=list[pygame.Surface], init=False)
    character_pos: list[tuple[int, int]] = field(default_factory=list[tuple[int, int]], init=False)
