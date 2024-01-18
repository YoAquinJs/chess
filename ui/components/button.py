"""This module contains the button object, which is the UI element for button interactions"""

# Import external libraries
import pygame
from collections.abc import Callable

# Import internal module
from game_logic.game_object import GameObject
from ui.components.sprite import Sprite
from ui.components.label import Label

class Button(GameObject):

    def __init__(self, x: int, y: int, sprite: Sprite, label: Label, callback: Callable) -> None:
        self.init_attributes()
        
        self._x = x
        self._y = y
        self.pressed = False
        self.callback = callback
        
        sprite.x = self.x
        sprite.y = self.y
        label.x = self.x
        label.y = self.y
        
        self.sprite = sprite
        self.add_child(0, sprite)
        self.add_child(1, label)

    @GameObject.x.setter
    def x(self, value):
        delta = value - self._x
        super().x.__set__(self, value)
        for child in self.children:
            child.x += delta

    @GameObject.y.setter
    def y(self, value):
        delta = value - self._y
        super().y.__set__(self, value)
        for child in self.children:
            child.y += delta

    def update(self):
        """Update the button pressed status, and call the callback when pressed
        """
        
        def overshadow(tint: tuple[int, int, int], increase: int):
            return (tint[0]-increase,tint[1]-increase,tint[2]-increase)
        
        mouseOnButton = self.sprite.rect.collidepoint(pygame.mouse.get_pos())
        leftClickPressed = pygame.mouse.get_pressed()[0]
        
        if self.pressed: # On realease
            if not mouseOnButton:
                self.pressed = False
            elif not leftClickPressed:
                self.pressed = False
                self.callback()

        tint = (255,255,255)
        if mouseOnButton:
            tint = overshadow(tint, 25)
            if leftClickPressed:
                tint = overshadow(tint, 30)
                self.pressed = True
        
        self.sprite.tint = tint

    def render(self, surface: pygame.Surface):
        pass
