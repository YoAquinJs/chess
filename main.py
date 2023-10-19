"""This module is the run file for the app, initializes all other modules"""

# Import external libraries
import pygame
from typing import Type, Union, Mapping, List
import datetime

# Import internal modules
from core.game_manager import GameManager
from core.consts import SCREEN_SIZE,  SPRITE
from user_interface.button import Button
from chess_engine.board import Board
from utils.utils import scale_image

if __name__ == "__main__":
    GameManager.init_game()
    while True:
        GameManager.update()
    #??# pygame setup
    #??pygame.init()
    #??screen = pygame.display.set_mode((1, 1))
    #??pygame.display.set_caption("CHESS")
    #??clock = pygame.time.Clock()

    #??# Get the background image and scale it
    #??background_img = scale_image(pygame.image.load(f"{SPRITE}background.png"))

    #??screen = pygame.display.set_mode((background_img.get_width(),background_img.get_height()))
    #??
    #??# Main Screen Buttons
    #??playBttImg = scale_image(pygame.image.load(f"{SPRITE}play-btt.png"),2)
    #??playButton = Button(playBttImg, "", screen.get_width()//2, screen.get_height()//3, None)
    #??quitBttImg = scale_image(pygame.image.load(f"{SPRITE}quit-btt.png"),2)
    #??quitButton = Button(quitBttImg, "", screen.get_width()//2, 2*(screen.get_height()//3), None)
    #??
    #??run = True
    #??update = True
    #??render = True
    #??while run:
    #??    # Run Events
    #??    for event in pygame.event.get():
    #??        if event.type == pygame.QUIT:
    #??            run = False
    #??
    #??    # Rendering
    #??    screen.blit(background_img, (0,0))
    #??    
    #??    # Update functions
    #??    if update:
    #??        playButton.update()
    #??        quitButton.update()
    #??    
    #??    # Render functions
    #??    if render:
    #??        playButton.render(screen)
    #??        quitButton.render(screen)
    #??
    #??    pygame.display.update()
    #??    clock.tick(60) # limits FPS to 60
    #??
    #??pygame.quit()