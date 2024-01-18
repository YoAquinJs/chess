import pygame

class Text():

    def __init__(self, text: str, scale: float=1) -> None:
        self.value = text
        self.scale = scale
        self.characterImages: list[pygame.Surface] = []
        self.renderPositions: list[tuple[int, int]] = []