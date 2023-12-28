"""This module is the run file for the app, initializes all other modules"""

# Import external libraries
import pygame
import datetime
from typing import Type, Union, Mapping, List

# Import internal modules
from core.game_manager import GameManager
from core.consts import SCREEN_SIZE,  SPRITE
from user_interface.button import Button
from user_interface.font import Font
from utils.utils import scale_image

if __name__ == "__main__":
    GameManager.init_game()
    
    # pygame setup
    pygame.init()    
    pygame.display.set_caption("CHESS")
    clock = pygame.time.Clock()
    
    # Get the background image and scale it
    background_img = scale_image(pygame.image.load(f"{SPRITE}background.png"))

    screenSize = (background_img.get_width(),background_img.get_height())
    screen = pygame.display.set_mode(screenSize,0,32)
    font = Font("assets/sprites/font.png")
    
    # Main Screen Buttons
    newGameBttImg = pygame.Surface((500,200))#scale_image(pygame.image.load(f"{SPRITE}play-btt.png"),2)
    newGameButton = Button(screen.get_width()//2, screen.get_height()//3, newGameBttImg, "NEW GAME", font, None)
    loadGameBttImg = pygame.Surface((300,100))#scale_image(pygame.image.load(f"{SPRITE}quit-btt.png"),2)
    loadGameButton = Button(screen.get_width()//2, 2*(screen.get_height()//3), loadGameBttImg, "LOAD GAME", font, None)
    
    run = True
    update = True
    render = True
    while run:
        # Run Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Rendering
        screen.blit(background_img, (0,0))
        
        # Update functions
        if update:
            newGameButton.update()
            loadGameButton.update()
        
        # Render functions
        if render:
            newGameButton.render(screen)
            loadGameButton.render(screen)

        pygame.display.flip()
        #GameManager.update()
        clock.tick(60) # limits FPS to 60
    
    pygame.quit()