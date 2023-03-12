from utils.observer import Observer
from gui.hud.hud_element import HudElement

import pygame


class ExperienceBar(HudElement, Observer):
    BAR_WIDTH = 300
    BAR_HEIGHT = 10

    def __init__(self):
        super().__init__()

    def setup(self, **kwargs):
        magic_level = kwargs["magic_level"]
        magic_level.add_listener(self)
        self.__update_bar(magic_level)

    def draw(self, screen):
        screen.blit(
            self.bar,
            (screen.get_width() / 2 - self.bar.get_width() / 2, 20),
        )

    def __update_bar(self, magic_level):
        self.bar = pygame.Surface((self.BAR_WIDTH, self.BAR_HEIGHT))
        self.bar.fill((40, 40, 40))

        percentage_exp = magic_level.get_exp() / magic_level.get_next_level_exp()
        exp_bar = pygame.Surface((percentage_exp * self.BAR_WIDTH, self.BAR_HEIGHT))
        exp_bar.fill((0, 255, 0))

        self.bar.blit(exp_bar, (0, 0))

    def notify(self, magic_level):
        self.__update_bar(magic_level)
