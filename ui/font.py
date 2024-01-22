"""This module contains the model class Font, for handling fonts and text rendering"""

from math import floor

import pygame

from game_logic.consts import CHAR_SEPARATOR, CHARACTER_ORDER
from ui.text import Text
from utils.utils import scale_img


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
    clip_r = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clip_r)
    image = surface.subsurface(handle_surf.get_clip())

    return image.copy()

class Font():
    """Font class for handling text rendering and importing Fonts
    """

    def __init__(self, font_path: str):
        """Returns a font object

        Args:
            fontPath (str): Path to the font image to be used.
        """
        self.characters: dict[str, pygame.Surface] = {}
        curr_char_width = 0
        count = 0

        font_img = pygame.image.load(font_path).convert_alpha()
        font_img_width, font_img_heigth = font_img.get_size()
        for x in range(font_img_width):
            c = font_img.get_at((x, 0))
            if c.r == CHAR_SEPARATOR:
                char_img = clip(font_img, x - curr_char_width, 0, curr_char_width, font_img_heigth)
                self.characters[CHARACTER_ORDER[count]] = scale_img(char_img, scale_to_screen=True)
                count += 1
                curr_char_width = 0
            else:
                curr_char_width += 1

        self.space_width = self.characters['A'].get_width()
        self.spacing = self.space_width//2

    def generate_text(self, text: Text, color: tuple[int, int, int]) -> None:
        """From the font object renders the text specified
        """
        if len(text.character_imgs) != 0 or len(text.character_positions) != 0:
            raise ValueError("Passed text object had been already generated")

        x_offset = 0
        for char in text.value:
            if char == ' ':
                x_offset += floor((self.space_width + self.spacing)*text.scale//2)
            else:
                char_img = scale_img(self.characters[char].copy(), text.scale, False)
                char_img.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

                text.character_imgs.append(char_img)
                text.character_positions.append((x_offset, 0))
                x_offset += floor((self.spacing*text.scale) + char_img.get_width())

    def render_text(self, x: int, y: int, text: Text, screen: pygame.Surface) -> None:
        """TODO
        """
        for char_img, coord in zip(text.character_imgs, text.character_positions):
            ix, iy = coord
            screen.blit(char_img, (x+ix, y+iy))

    def center_text_coords(self, x: int, y: int, text: Text) -> tuple[int, int]:
        """TODO
        """
        scaled_space = self.spacing*text.scale
        width = sum(char_img.get_width()+scaled_space for char_img in text.character_imgs)
        x -= floor(width/2)

        upper_char_middle, lower_char_middle = 6/16, 8/16
        has_any_upper = any(char.isalpha() and char.isupper() for char in text.value)
        middle_char_heigth = upper_char_middle if has_any_upper else lower_char_middle
        y -= floor(self.characters["A"].get_height()*text.scale*middle_char_heigth)

        return x, y
