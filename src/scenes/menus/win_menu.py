import random
import pygame

from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from constants.gui_constants import COLOR_BRIGHT, COLOR_STANDARD, COLOR_SUBTLE
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from scenes.menus.vertical_menu import VerticalMenu
from systems.resource_manager import Resource
from systems.rng_system import RngSystem


class WinMenu(VerticalMenu):
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
        veil.set_alpha(10)

        background = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        background.blit(background_image, (0, 0))
        background.blit(veil, (0, 0))
        self.background = background

        self.scene_music = Resource.WIN_MUSIC

        self.title_words = [
            "Awesome",
            "Spectacular",
            "Fantastic",
            "Great",
            "Amazing",
            "Superb",
            "Brilliant",
            "Incredible",
            "Marvelous",
            "Wonderful",
            "Magnificent",
            "Stupendous",
            "Astounding",
            "Remarkable",
            "Extraordinary",
            "Exceptional",
            "Outstanding",
        ]

        self.subtitle_phrases = [
            "You made an awesome job!",
            "You are a true hero!",
            "You are a true champion!",
            "You conquer the planet!",
            "You are the best!",
            "You are the best in the universe!",
            "You are the best in the galaxy!",
        ]

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

    def __get_random_title(self):
        return random.choice(self.title_words)

    def __get_random_subtitle(self):
        return random.choice(self.subtitle_phrases)

    def setup(self):
        self.title = Title(
            text=f"{self.__get_random_title()} win!",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 150),
        )

        self.subtitle = Title(
            text=self.__get_random_subtitle(),
            font=self.resource_manager.load_font(Resource.FONT_MD),
            color=COLOR_STANDARD,
            position=(DESIGN_WIDTH / 2, 220),
        )

        self.buttons.append(self.__create_button("Back to menu", self.__main_menu, 0))

        self.gui_group.add(self.title, self.subtitle, self.buttons)
        super().setup()
