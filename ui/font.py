"""This module contains the model class Font, for handling fonts and text rendering"""

import pygame
from pygame.locals import *

from utils.utils import scale_image
from game_logic.consts import CHARACTER_ORDER, CHAR_SEPARATOR
from ui.text import Text

def clip(surface: pygame.Surface, x: int, y: int, x_size: int, y_size: int) -> pygame.Surface:
    """Clips an image from a surface

    Args:
        surface (pygame.Surface): Surface to clip from.
        x (int): Position in X.
        y (int): Position in Y.
        x_size (int): Size in X.
        y_size (int): Size in Y
    
    Returns:
        pygame.Surface: Image cliped
    """
    
    handle_surf = surface.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surface.subsurface(handle_surf.get_clip())
    
    return image.copy()

class Font():
    """Font class for handling text rendering and importing Fonts
    """

    def __init__(self, fontPath: str):
        """Returns a font object

        Args:
            fontPath (str): Path to the font image to be used.
        """
        
        self.characters: dict[str, pygame.Surface] = {}
        current_char_width = 0
        count = 0
        
        font_img = pygame.image.load(fontPath).convert_alpha()
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c.r == CHAR_SEPARATOR:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[CHARACTER_ORDER[count]] = scale_image(char_img, scaleToScreen=True)
                count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        
        self.space_width = self.characters['A'].get_width()
        self.spacing = self.space_width//2

    def generate_text(self, text: Text, color: tuple[int, int, int]) -> None:
        """From the font object renders the text specified
        """
        
        if len(text.characterImages) != 0 or len(text.renderPositions) != 0:
            raise ValueError("Passed text object had been already generated")

        x_offset = 0
        for char in text.value:
            if char == ' ':
                x_offset += (self.space_width + self.spacing)*text.scale/2
            else:
                charImg = scale_image(self.characters[char].copy(), text.scale, False)
                charImg.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
                
                text.characterImages.append(charImg)
                text.renderPositions.append((x_offset, 0))
                x_offset += (self.spacing*text.scale) + charImg.get_width()

    def render_text(self, x: int, y: int, text: Text, screen: pygame.Surface, centered=True) -> None:
        if centered:
            width = sum(charImg.get_width()+self.spacing*text.scale for charImg in text.characterImages)
            x -= width//2
            
            middle_char_heigth = 6/16 if any(char.isalpha() and char.isupper() for char in text.value) else 8/16
            y -= self.characters["A"].get_height()*text.scale*middle_char_heigth
        
        for charImg, coord in zip(text.characterImages, text.renderPositions):
            iX, iY = coord
            screen.blit(charImg, (x+iX, y+iY))
