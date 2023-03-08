import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.button import Button
from gui.title import Title
from gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menu.configuration_menu import ConfigurationMenu
from scenes.menu.menu import Menu
from systems.resource_manager import Resource


class PauseMenu(Menu):
    def __init__(self):
        super().__init__()
        background = self.director.virtual_screen.copy()
        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(200)
        background.blit(veil, (0, 0))
        self.background = background

    def __resume_game(self):
        self.director.pop_scene()

    def __leave_game(self):
        self.director.leave_game()

    def __config_game(self):
        self.director.push_scene(ConfigurationMenu())

    def __create_button(self, text, action, offset):
        font = self.resource_manager.load_font(Resource.FONT_LG)
        return Button(
            text=text,
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=action,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 + offset),
        )

    def setup(self):
        self.title = Title(
            text="Pause",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 100),
        )

        self.buttons.append(self.__create_button("Resume", self.__resume_game, -100))
        self.buttons.append(
            self.__create_button("Configuration", self.__config_game, 0)
        )
        self.buttons.append(self.__create_button("Quit Game", self.__leave_game, 100))

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__resume_game()
