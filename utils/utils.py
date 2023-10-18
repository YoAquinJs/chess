import json
from datetime import datetime
from typing import Union
import pygame

from core.consts import PrintColor, PlayerColor, SCREEN_SIZE

def get_timestamp() -> str:
    """Retorna el tiempo y hora actual

    Returns:
        srt: String Del Tiempo Actual
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

def scale_image(image: pygame.image, scale: float = 1) -> pygame.image:
    """Scales the image in the given path

    Args:
        image (pygame.image): Image to be scaled.
        scale (float, optional): Scales the image, default to 1, the screen scale. Defaults to 1.

    Returns:
        pygame.image: Image object scaled
    """
    
    return pygame.transform.scale(image, (image.get_width()*SCREEN_SIZE*scale,image.get_height()*SCREEN_SIZE*scale))
