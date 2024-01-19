import pygame

from utils.utils import scale_image, get_asset_path
from game_logic.scene import Scene, SceneBaseData
from game_logic.consts import AssetType
from ui.font import Font
from ui.elements.label import Label
from ui.elements.button import Button
from ui.elements.sprite import Sprite
from ui.elements.labeled_sprite import LabeledSprite
from ui.text import Text

# Back to main menu button
# Display the saved games

class LoadGameScene(Scene):

    def __init__(self, baseData: SceneBaseData) -> None:
        super().__init__(baseData)
        
        # Background
        backgroundImg = Sprite(0, 0, scale_image(pygame.image.load(get_asset_path(AssetType.sprite, "background.png"))))
        
        img = pygame.Surface((400,95))
        img.fill((255,0,0))
        label = Label(0, 0, Text("New Game", 1.2), (0,0,255), self.font)
        labeledSprite = LabeledSprite(300, 100, label, img, pixelByPixel=False, centered=True)

        # Hierarchy
        self.register_obj(backgroundImg)
        self.register_obj(labeledSprite)
