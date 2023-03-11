import pygame

from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from utils.observer import Observer


class ExperienceBar(Observer):
    def __init__(self):
        super().__init__()

    def setup(self, magic_level):
        magic_level.add_listener(self)
        self.__update_bar(magic_level)

    def __update_bar(self, magic_level):
        bar_width = 300
        bar_height = 10
        self.bar = pygame.Surface((bar_width, bar_height))
        self.bar.fill((40, 40, 40))

        percentage_exp = magic_level.get_exp() / magic_level.get_next_level_exp()
        exp_bar = pygame.Surface((percentage_exp * bar_width, bar_height))
        exp_bar.fill((0, 255, 0))

        self.bar.blit(exp_bar, (0, 0))

    def get_surface(self):
        return self.bar

    def notify(self, magic_level):
        self.__update_bar(magic_level)


class Hud:
    def __init__(self):
        self.exp_bar = ExperienceBar()

    def setup(self, player):
        self.exp_bar.setup(player.magic_level)

    def draw(self, screen):
        exp_bar = self.exp_bar.get_surface()
        screen.blit(
            exp_bar,
            (screen.get_width() / 2 - exp_bar.get_width() / 2, 20),
        )
