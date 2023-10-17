import json
from datetime import datetime
from typing import Union

from models.consts import PrintColor, PlayerColor

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