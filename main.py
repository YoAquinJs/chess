"""This module is the run file for the app, initializes all other modules"""

# Import external libraries
import pygame

# Import internal modules
from core.consts import AssetType
from screens.main_menu import MainMenuScreen
from utils.utils import scale_image, get_asset_path
from user_interface.font import Font
from core.game_manager import GameManager

def pygame_setup() -> tuple[pygame.time.Clock, pygame.Surface]:
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("CHESS")
    
    backgroundImg = scale_image(pygame.image.load(get_asset_path(AssetType.sprite, "background.png")))
    screenSize = (backgroundImg.get_width(),backgroundImg.get_height())
    screen = pygame.display.set_mode(screenSize)

    iconImg = pygame.image.load(get_asset_path(AssetType.sprite, "icon.png")).convert_alpha()
    pygame.display.set_icon(iconImg)
    
    return clock, screen

def main():
    clock, screen = pygame_setup()

    font = Font(get_asset_path(AssetType.sprite, "font.png"))
    
    GameManager.init_game(screen, font, MainMenuScreen)
    while GameManager.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameManager.quit()
        
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
