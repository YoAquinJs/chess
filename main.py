import pygame
from typing import Type, Union, Mapping, List
import datetime

from models.board import Board

#board = Board.start_board()
#board.serialize("data")
#board.swap_pieces(0,3,3,3)
#board.print_board()
#board.get_valid_movements(board.select_square(3,3))
board = Board.deserialize("data")
print(board.canCastle)
print(board.possibleEnPassant)
print(board.turn)
print(board.canCastle)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#?while running:
#?    # poll for events
#?    # pygame.QUIT event means the user clicked X to close your window
#?    for event in pygame.event.get():
#?        if event.type == pygame.QUIT:
#?            running = False
#?
#?    # fill the screen with a color to wipe away anything from last frame
#?    screen.fill("white")
#?
#?    # RENDER YOUR GAME HERE
#?
#?    # flip() the display to put your work on screen
#?    pygame.display.flip()
#?
#?    clock.tick(60)  # limits FPS to 60

pygame.quit()