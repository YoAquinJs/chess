"""Main menu scene"""

import pygame

from game_logic.consts import AssetType
from game_logic.game_manager import GameManager
from scenes.load_game import LoadGameScene
from scenes.on_game import OnGameScene
from ui.elements.button import Button, ButtonInitData
from ui.elements.label import Label, LabelInitData
from ui.elements.sprite import Sprite, SpriteInitData
from ui.scene import Scene, SceneBaseData
from ui.text import Text
from utils.utils import get_asset_path, scale_img


class MainMenuScene(Scene):
    """TODO
    """
    def __init__(self, baseData: SceneBaseData) -> None:
        super().__init__(baseData)

        # Background
        img = scale_img(pygame.image.load(get_asset_path(AssetType.SPRITE, "background.png")))
        background_img = Sprite(0, 0, SpriteInitData(img))

        # New Game Button
        x = self.screen.get_width()//2
        y = self.screen.get_height()//3
        img = pygame.Surface((400,95))
        img.fill((255,0,0))
        sprite = Sprite(0, 0, SpriteInitData(img, pixel_tint=False, centered=True))
        label = Label(0, 0, LabelInitData(Text("New Game", 1.2), (0,0,255), self.font))
        init_data = ButtonInitData(sprite, label, lambda: GameManager.load_screen(OnGameScene))
        new_game_btt = Button(x, y, init_data)

        # Load Game Button
        x = self.screen.get_width()//2
        y = int(1.5*(self.screen.get_height()//3))
        img = pygame.Surface((400,80))
        img.fill((255,0,0))
        sprite = Sprite(0, 0, SpriteInitData(img, pixel_tint=False, centered=True))
        label = Label(0, 0, LabelInitData(Text("Load Game"), (0,0,0), self.font))
        init_data = ButtonInitData(sprite, label, lambda: GameManager.load_screen(LoadGameScene))
        load_game_btt = Button(x, y, init_data)

        # Hierarchy
        self.register_obj(background_img)
        self.register_obj(new_game_btt)
        self.register_obj(load_game_btt)
