from dataclasses import dataclass
import pygame

@dataclass
class Text():
    value: str
    scale: float
    characterImages: list[pygame.Surface] = []
    renderPositions: list[tuple[int, int]] = []
