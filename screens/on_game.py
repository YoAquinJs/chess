import pygame

from utils.utils import scale_image, get_asset_path
from core.screen import Screen
from core.consts import AssetType
from user_interface.font import Font
from user_interface.label import Label
from user_interface.button import Button
from user_interface.sprite import Sprite
from user_interface.text import Text

# New Background
# Board objects
# Turn label
# Status label
# Move history display
# Save game button
# Delete game button

class OnGameScreen(Screen):

    def init_objects(self):
        # Background
        backgroundImg = Sprite(0, 0, scale_image(pygame.image.load(get_asset_path(AssetType.sprite, "background.png"))))
        
        labelTest = Label(0, 0, Text("On Game", 3), (255,0,0), self.font, centered=False)
        
        # Hierarchy
        self.register_obj(backgroundImg)
        self.register_obj(labelTest)
