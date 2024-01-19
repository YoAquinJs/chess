from dataclasses import dataclass, field
import pygame

@dataclass
class Text():
    value: str
    scale: float
    characterImages: list[pygame.Surface] = field(default_factory=list[pygame.Surface])
    renderPositions: list[tuple[int, int]] = field(default_factory=list[tuple[int, int]])
