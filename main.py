"""This module is the run file for the app, initializes all other modules"""

# Import external libraries
import pygame

# Import internal modules
from core.consts import AssetType
from utils.utils import scale_image, get_asset_path
from user_interface.font import Font
from core.game_manager import GameManager

def main():
    # pygame setup
    pygame.init()
    pygame.display.set_caption("CHESS")
    clock = pygame.time.Clock()
    
    # Get the background image and scale it
    background_img = scale_image(pygame.image.load(get_asset_path(AssetType.sprite, "background.png")))
    
    screenSize = (background_img.get_width(),background_img.get_height())
    screen = pygame.display.set_mode(screenSize)
    font = Font(get_asset_path(AssetType.sprite, "font.png"))
    
    GameManager.init_game(screen, font)
    while GameManager.running:
        # Run Events
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
