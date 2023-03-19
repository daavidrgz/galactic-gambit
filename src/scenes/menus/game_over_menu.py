import pygame

from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from scenes.menus.vertical_menu import VerticalMenu
from systems.resource_manager import Resource
from systems.rng_system import RngSystem


class GameOverMenu(VerticalMenu):
    def __init__(self):
        super().__init__()
        background_image = self.resource_manager.load_image(Resource.PLANETS_BG)
        bg_width, bg_height = background_image.get_size()
        background_image = pygame.transform.scale(
            background_image,
            (
                (DESIGN_HEIGHT / bg_height) * bg_width,
                DESIGN_HEIGHT,
            ),
        )

        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(40)

        background = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        background.blit(background_image, (0, 0))
        background.blit(veil, (0, 0))
        self.background = background

        self.scene_music = Resource.GAME_OVER_MUSIC

    def __main_menu(self):
        RngSystem().new_seed()
        self.director.pop_scene()

    def __create_button(self, text, action, offset):
        font = self.resource_manager.load_font(Resource.FONT_LG)
        return TextButton(
            text=text,
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=action,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 + offset),
        )

    def setup(self):
        self.title = Title(
            text="Game Over",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 150),
        )

        self.buttons.append(self.__create_button("Back to menu", self.__main_menu, 0))

        self.gui_group.add(self.title, self.buttons)
        super().setup()
