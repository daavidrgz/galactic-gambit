from constants.gui_constants import COLOR_BRIGHT
from systems.resource_manager import Resource
from utils.observer import Observer
from gui.hud.hud_element import HudElement

import pygame


class ExperienceBar(HudElement, Observer):
    BAR_WIDTH = 300
    BAR_HEIGHT = 2.5

    def __init__(self):
        super().__init__()
        self.font = self.resource_manager.load_font(Resource.FONT_SM)
        self.level_text = None
        self.bar = None

    def setup(self, **kwargs):
        magic_level = kwargs["magic_level"]
        magic_level.add_listener(self)
        self.__update_component(magic_level)

    def draw(self, screen):
        screen.blit(
            self.level_text,
            (screen.get_width() / 2 - self.level_text.get_width() / 2, 10),
        )

        screen.blit(
            self.bar,
            (
                screen.get_width() / 2 - self.bar.get_width() / 2,
                30 - self.bar.get_height() / 2,
            ),
        )

    def __update_component(self, magic_level):
        self.__update_bar(magic_level)
        self.__update_level(magic_level)

    def __update_bar(self, magic_level):
        self.bar = pygame.Surface((self.BAR_WIDTH, self.BAR_HEIGHT))
        self.bar.fill((40, 40, 40))

        if magic_level.is_max_level() or magic_level.get_next_level_exp() == 0:
            percentage_exp = 1
        else:
            percentage_exp = magic_level.get_exp() / magic_level.get_next_level_exp()
        exp_bar = pygame.Surface((percentage_exp * self.BAR_WIDTH, self.BAR_HEIGHT))
        exp_bar.fill((0, 255, 255))

        self.bar.blit(exp_bar, (0, 0))

    def __update_level(self, magic_level):
        if magic_level.is_max_level():
            text = "Max level"
        else:
            text = f"Exp level {magic_level.get_level()}"
        self.level_text = self.font.render(text, True, COLOR_BRIGHT)

    def notify(self, magic_level):
        self.__update_component(magic_level)
