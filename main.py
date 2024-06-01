"""This module is the run file for the app, initializes all other modules"""

# Execute
# py main.py

# Run tests
# py -m pytest

# Import external libraries
import pygame

from game_logic.consts import AssetType
from game_logic.game_manager import GameManager
from scenes.main_menu import MainMenuScene
from ui.font import Font
from utils.utils import get_asset_path, scale_img


def pygame_setup() -> tuple[pygame.time.Clock, pygame.Surface]:
    """Initialize pygame and return the clock and screen

    Returns:
        tuple[pygame.time.Clock, pygame.Surface]: Clock and screen surface
    """
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("CHESS")

    bacground_img_path = get_asset_path(AssetType.SPRITE, "background.png")
    background_img = scale_img(pygame.image.load(bacground_img_path))
    scree_size = (background_img.get_width(),background_img.get_height())
    screen = pygame.display.set_mode(scree_size)

    icon_img = pygame.image.load(get_asset_path(AssetType.SPRITE, "icon.png")).convert_alpha()
    pygame.display.set_icon(icon_img)

    return clock, screen

def main() -> None:
    """Program executer
    """
    clock, screen = pygame_setup()

    font = Font(get_asset_path(AssetType.SPRITE, "font.png"))

    GameManager.init_game(screen, font, MainMenuScene)
    while GameManager.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameManager.quit()

            for game_event in GameManager

        # Game logic
        GameManager.update()

        # Rendering
        screen.fill((0,0,0))
        GameManager.render()
        pygame.display.flip()

        # limits FPS to 60
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
