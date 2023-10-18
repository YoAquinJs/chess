"""This module contains the button object, which is the UI element for button interactions"""

# Import external libraries
import pygame
from collections.abc import Callable

# Import internal module
from user_interface.font import Font

class Button():
    """Class for handling button interaction in the UI

        Attributes:
            image (pygame.image): Button image.
            text (str): Button text.
            rect (pygame.rect): Button rect in surface.
            callback (Callable): Button callback action.
            pressed (bool): Button pressed state.
            
    """

    def __init__(self, image: pygame.image, text: str, x: int, y: int, callback: Callable) -> None:
        """Creates a button object

        Args:
            image (pygame.image): The pygame image of the button.
            text (str): Button label.
            x (int): Position in X.
            y (int): Position in Y.
            callback (Callable): The action to be executed when the button is pressed
        """
        
        self.image = image
        self.text = text
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.callback = callback
        
        self.pressed = False
        
    def update(self):
        """Update the button pressed status, and call the callback when pressed
        """
        
        mouse = pygame.mouse.get_pos()
        leftClickPressed = pygame.mouse.get_pressed()[0]
        
        if self.rect.collidepoint(mouse) and leftClickPressed and not self.pressed: # On Press
            self.pressed = True
        elif not leftClickPressed and self.pressed: # On realease
            self.pressed = False
            self.callback()
                
    def render(self, surface: pygame.surface, font: Font):
        """Render the button image and text to the screen

        Args:
            surface (pygame.surface): Surface in which to render.
            font (Font): Font to use for text rendering
        """
        
        font.render(surface, self.text, (self.rect.x, self.rect.y))
        surface.blit(self.image, (self.rect.x, self.rect.y))
        