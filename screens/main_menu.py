import pygame
from typing import Type

from utils.utils import scale_image, get_asset_path
from game_logic.consts import AssetType
from game_logic.screen import Screen
from screens.on_game import OnGameScreen
from screens.load_game import LoadGameScreen
from ui.text import Text
from ui.elements.label import Label
from ui.elements.button import Button
from ui.elements.sprite import Sprite
from game_logic.game_manager import GameManager

class MainMenuScreen(Screen):

    def init_objects(self) -> None:
        # Background
        backgroundSprite = Sprite(0, 0, scale_image(pygame.image.load(get_asset_path(AssetType.sprite, "background.png"))))
        
        # New Game Button
        newGameBttX = self.renderScreen.get_width()//2
        newGameBttY = self.renderScreen.get_height()//3
        img = pygame.Surface((400,95))
        img.fill((255,0,0))
        newGameBttSprite = Sprite(0, 0, img, pixelByPixel=False, centered=True)
        newGameBttLabel = Label(0, 0, Text("New Game", 1.2), (0,0,255), self.font)
        newGameButton = Button(newGameBttX, newGameBttY, newGameBttSprite, newGameBttLabel, lambda: GameManager.load_screen(OnGameScreen))
        
        # Load Game Button
        loadGameBttX = self.renderScreen.get_width()//2
        loadGameBttY = 1.5*(self.renderScreen.get_height()//3)
        img = pygame.Surface((400,80))
        img.fill((255,0,0))
        loadGameSprite = Sprite(0, 0, img, pixelByPixel=False, centered=True)
        loadGameLabel = Label(0, 0, Text( "Load Game"), (0,0,0), self.font)
        loadGameButton = Button(loadGameBttX, loadGameBttY, loadGameSprite, loadGameLabel, lambda: GameManager.load_screen(LoadGameScreen))
        
        # Hierarchy
        self.register_obj(backgroundSprite)
        self.register_obj(newGameButton)
        self.register_obj(loadGameButton)
