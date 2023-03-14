import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.configuration_menu import ConfigurationMenu
from scenes.menus.vertical_menu import VerticalMenu
from scenes.transition import Transition
from systems.resource_manager import Resource


class PauseMenu(VerticalMenu):
    def __init__(self):
        super().__init__()
        background = self.director.virtual_screen.copy()
        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(220)
        background.blit(veil, (0, 0))
        self.background = background

    def __resume_game(self):
        self.director.pop_scene()

    def __return_to_menu(self):
        self.director.pop_scene()
        self.director.pop_scene()

    def __quit_game(self):
        self.director.leave_game()

    def __config_game(self):
        self.director.push_scene(ConfigurationMenu(self.background))

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
            text="Pause",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 100),
        )

        self.buttons.append(self.__create_button("Resume", self.__resume_game, -150))
        self.buttons.append(
            self.__create_button("Configuration", self.__config_game, -50)
        )
        return_menu_button = self.__create_button(
            "Return to menu", self.__return_to_menu, 50
        )
        return_menu_button.confirm_sound = Resource.GO_BACK_ALT_SOUND
        self.buttons.append(return_menu_button)
        self.buttons.append(self.__create_button("Quit game", self.__quit_game, 150))

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__resume_game()
