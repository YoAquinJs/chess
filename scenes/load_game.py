"""Load game scene"""

import pygame

from game_logic.consts import AssetType
from ui.scene import Scene, SceneBaseData
from ui.elements.sprite import Sprite, SpriteInitData
from utils.utils import get_asset_path, scale_img

# Back to main menu button
# Display the saved games

class LoadGameScene(Scene):
    """TODO
    """
    def __init__(self, baseData: SceneBaseData) -> None:
        super().__init__(baseData)

        # Background
        img = scale_img(pygame.image.load(get_asset_path(AssetType.SPRITE, "background.png")))
        background_img = Sprite(0, 0, SpriteInitData(img))

        # Hierarchy
        self.register_obj(background_img)
