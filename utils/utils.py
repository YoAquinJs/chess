"""This module contain utilities that are available app wide"""

# Import external libraries
import pygame
from os import path
from core.consts import AssetType

# Import internal module
from core.consts import PrintColor, PlayerColor, SCREEN_SIZE

def color_print(text: str, color: PrintColor, end='\n'):
    """Prints to console with the color specified

    Args:
        text (str): Text to print
        color (PrintColor): Color to print with
        end (str, optional): End of print. Defaults to '\n'.
    """
    
    print(color.value + text + PrintColor.reset.value, end=end)
    
def opponent(player: PlayerColor) -> PlayerColor:
    """Returns the opponent of the specified player color

    Args:
        player (PlayerColor): Player.

    Returns:
        PlayerColor: The opponent of player
    """
    
    return PlayerColor.black if player == PlayerColor.white else PlayerColor.white

def scale_image(image: pygame.Surface, scale: float = 1, scaleToScreen: bool = True) -> pygame.Surface:
    """Scales the image in the given path

    Args:
        image (pygame.Surface): Image to be scaled.
        scale (float, optional): Scales the image, default to 1, the screen scale. Defaults to 1.

    Returns:
        pygame.Surface: Image object scaled
    """
    
    if scaleToScreen:
        scale *= SCREEN_SIZE
    return pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

def tint_image(image: pygame.Surface, tint: tuple[int, int, int]) -> None:
    """Tints the given image
    
    Args:
        image (pygame.Surface): Image.
        tint (tuple[int, int, int]): Tint color.
    """
    
    image.fill(tint)

def get_asset_path(type: AssetType, *subPaths: str) -> str:
    """Return the path of an asset based on the type and sub path

    Args:
        type (AssetType): Type of the asset to look for

    Returns:
        str: Built path.
    """
    
    return path.join(type.value, *subPaths)
