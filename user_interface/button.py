import pygame

class Button():
    def __init__(self, image: pygame.image, x: int, y: int, callback: function) -> None:
        """Creates a button object

        Args:
            image (pygame.image): The pygame image of the button.
            x (int): The button screen position in x.
            y (int): The button screen position in y.
            callback (function): The action to be executed when the button is pressed
        """
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.callback = callback
        
        self.pressed = False
        
        
    def update(self):
        mouse = pygame.mouse.get_pos()
        leftClickPressed = pygame.mouse.get_pressed()[0]
        
        if self.rect.collidepoint(mouse) and leftClickPressed and not self.pressed: # On Press
            self.pressed = True
        elif not leftClickPressed and self.pressed: # On realease
            self.pressed = False
            self.callback()
                
    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        