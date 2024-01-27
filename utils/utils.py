"""This module contain utilities that are available app wide"""

# Import external libraries
from math import floor
from os import path

import pygame

from chess_engine.piece import SideColor
# Import internal module
from game_logic.consts import SCREEN_SIZE, AssetType, PrintColor


def color_print(text: str, color: PrintColor, end: str='\n') -> None:
    """Prints to console with the color specified

    Args:
        text (str): Text to print
        color (PrintColor): Color to print with
        end (str, optional): End of print. Defaults to '\n'.
    """
    print(color.value + text + PrintColor.RESET.value, end=end)

def opponent(player: SideColor) -> SideColor:
    """Returns the opponent of the specified player color

    Args:
        player (PlayerColor): Player.

    Returns:
        PlayerColor: The opponent of player
    """
    return SideColor.BLACK if player == SideColor.WHITE else SideColor.WHITE

def scale_img(image: pygame.Surface, scale: float=1, scale_to_screen: bool=True) -> pygame.Surface:
    """Scales the image in the given path

    Args:
        image (pygame.Surface): Image to be scaled.
        scale (float, optional): Scales the image, default to 1, the screen scale. Defaults to 1.

    Returns:
        pygame.Surface: Image object scaled
    """
    if scale_to_screen:
        scale *= SCREEN_SIZE
    return pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

def tint_image(image: pygame.Surface, tint: tuple[int, int, int], pixel_tint: bool = False) -> None:
    """Tints the provided image

    Args:
        image (pygame.Surface): Image
        tint (tuple[int, int, int]): Tint
        pixel_tint (bool, optional): Whether to tint pixel by pixel or by fill. Defaults to False.
    """
    percentage_tint = tuple(t/255 for t in tint+(255,))
    if not pixel_tint:
        img_color = image.get_at((0,0))
        img_color = (img_color.r, img_color.g, img_color.b, img_color.a)
        new_color = tuple(floor(c*t) for c, t in zip(img_color, percentage_tint))
        image.fill(new_color, special_flags=pygame.BLEND_RGBA_MULT)
    else:
        for x, y in zip(range(image.get_width()), range(image.get_height())):
            pixel_color = image.get_at((x,y))
            pixel_color = (pixel_color.r, pixel_color.g, pixel_color.b, pixel_color.a)
            new_pixel_color = tuple(floor(c*t) for c, t in zip(pixel_color, percentage_tint))
            image.set_at((x,y), new_pixel_color)

def get_asset_path(asset_type: AssetType, *sub_paths: str) -> str:
    """Return the path of an asset based on the type and sub path

    Args:
        type (AssetType): Type of the asset to look for

    Returns:
        str: Built path.
    """
    return path.join(asset_type.value, *sub_paths)
