import pygame

from utils.utils import scale_image, get_asset_path
from game_logic.screen import Screen, ScreenBaseData
from game_logic.consts import AssetType
from ui.font import Font
from ui.text import Text
from ui.elements.label import Label
from ui.elements.button import Button
from ui.elements.sprite import Sprite

# New Background
# Board objects
# Turn label
# Status label
# Move history display
# Save game button
# Delete game button

class OnGameScreen(Screen):

    def __init__(self, baseData: ScreenBaseData) -> None:
        super().__init__(baseData)
        
        # Background
        backgroundImg = Sprite(0, 0, scale_image(pygame.image.load(get_asset_path(AssetType.sprite, "background.png"))))
        
        labelTest = Label(0, 0, Text("On Game", 3), (255,0,0), self.font, centered=False)
        
        # Hierarchy
        self.register_obj(backgroundImg)
        self.register_obj(labelTest)
