from systems.resource_manager import Resource
from utils.observer import Observer
from gui.hud.hud_element import HudElement

import pygame


class HealthBar(HudElement, Observer):
    BAR_WIDTH = 300
    BAR_HEIGHT = 20

    def __init__(self):
        super().__init__()
        self.font = self.resource_manager.load_font(Resource.FONT_SM)

    def setup(self, **kwargs):
        hp = kwargs["hp"]
        hp.add_listener(self)
        self.__update_bar(hp)

    def draw(self, screen):
        screen.blit(
            self.bar,
            (10, 20),
        )

    def __update_bar(self, hp):
        self.bar = pygame.Surface((self.BAR_WIDTH, self.BAR_HEIGHT))
        self.bar.fill((40, 40, 40))

        percentage_hp = hp.get_hp() / hp.get_max_hp()
        hp_bar = pygame.Surface((percentage_hp * self.BAR_WIDTH, self.BAR_HEIGHT))
        hp_bar.fill((0, 255, 0))

        self.bar.blit(hp_bar, (0, 0))

        health_text = self.font.render("Health", True, (255, 255, 255))

        self.bar.blit(
            health_text,
            (
                10,
                self.BAR_HEIGHT / 2 - health_text.get_height() / 2 + 2,
            ),
        )

        hp_text = self.font.render(f"{hp.get_hp()}", True, (255, 255, 255))

        self.bar.blit(
            hp_text,
            (
                self.BAR_WIDTH - hp_text.get_width() - 10,
                self.BAR_HEIGHT / 2 - hp_text.get_height() / 2 + 2,
            ),
        )

    def notify(self, hp):
        self.__update_bar(hp)
