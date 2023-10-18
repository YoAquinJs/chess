"""This module contains the model class Font, for handling fonts and text rendering"""

import pygame, sys
from pygame.locals import *

from utils.utils import scale_image
    
def clip(surface: pygame.surface, x: int, y: int, x_size: int, y_size: int) -> pygame.image:
    """Clips an image from a surface

    Args:
        surface (pygame.surface): Surface to clip from.
        x (int): Position in X.
        y (int): Position in Y.
        x_size (int): Size in X.
        y_size (int): Size in Y

    Returns:
        pygame.image: Image cliped
    """
    
    handle_surf = surface.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surface.subsurface(handle_surf.get_clip())
    
    return image.copy()

class Font():
    """Font class for handling text rendering and importing Fonts
    
        Attributes:
            spacing (int): Spacing between chars.
            character_order (List[str]): List of the order of the chars in the imported font.
            character_order (Dict[str, pygame.image]): Dictinary of char to it's corresponding image
            space_width (int): Width of a char image.
    """
    
    def __init__(self, fontPath: str):
        """Returns a font object

        Args:
            fontPath (str): Path to the font image to be used.
        """
        
        self.spacing = 1 
        current_char_width = 0
        self.characters = {}
        character_count = 0
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        
        font_img = pygame.image.load(fontPath).convert()
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
                
        self.space_width = self.characters['A'].get_width()

    def render(self, surface: pygame.Surface, text: str, x: int, y: int, scale: int=1):
        """From the font object renders the text specified

        Args:
            surface (pygame.Surface): Surface in which to render.
            text (str): Text to be rendered
            x (int): Position in X.
            y (int): Position in Y.
            scale(int, optional): Scaling of the resulting text image, Defaults to 1.
        """
        
        # Render char by char to screen
        x_offset = 0
        for char in text:
            if char != ' ':
                surface.blit(scale_image(self.characters[char], scale), (x + x_offset, y))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
