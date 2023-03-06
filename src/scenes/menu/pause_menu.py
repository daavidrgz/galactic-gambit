import itertools
import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.button import Button
from gui.title import Title
from scenes.menu.menu import Menu


class PauseMenu(Menu):
    def __init__(self):
        super().__init__()
        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(200)
        self.background = veil

    def __resume_game(self):
        self.director.pop_scene()

    def __leave_game(self):
        self.director.leave_game()

    def __config_game(self):
        pass

    def setup(self):
        subtle = (100, 100, 100)
        bright = (255, 255, 255)
        font = self.resource_manager.load_font(self.resource_manager.FONT_LG)

        self.title = Title(
            text="Pause",
            font=self.resource_manager.load_font(self.resource_manager.FONT_XL),
            color=bright,
            position=(DESIGN_WIDTH / 2, 100),
        )

        self.resume_button = Button(
            text="Resume",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__resume_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 - 100),
        )

        self.config_game_button = Button(
            text="Configuration",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__config_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.quit_game_button = Button(
            text="Quit Game",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__leave_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 + 100),
        )

        self.buttons.append(self.resume_button)
        self.buttons.append(self.config_game_button)
        self.buttons.append(self.quit_game_button)

        self.buttons_len = len(self.buttons)
        self.buttons[0].select()

        self.gui_group.add(self.title, self.buttons)

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__resume_game()
