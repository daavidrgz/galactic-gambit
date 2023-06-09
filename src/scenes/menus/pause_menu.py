import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from constants.gui_constants import BACKGROUND_COLOR, COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.confirmation_menu import ConfirmationMenu
from scenes.menus.in_game_configuration_menu import InGameConfigurationMenu
from scenes.menus.vertical_menu import VerticalMenu
from systems.resource_manager import Resource
from systems.rng_system import RngSystem


class PauseMenu(VerticalMenu):
    def __init__(self):
        super().__init__()
        background = self.director.virtual_screen.copy()
        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.fill(BACKGROUND_COLOR)
        veil.set_alpha(210)
        background.blit(veil, (0, 0))
        self.background = background

    def __resume_game(self):
        self.director.pop_scene()

    def __return_to_menu(self):
        def action():
            RngSystem().new_seed()
            self.director.pop_scene()
            self.director.pop_scene()

        self.director.push_scene(ConfirmationMenu(action, self.background))

    def __quit_game(self):
        def action():
            self.director.leave_game()

        self.director.push_scene(ConfirmationMenu(action, self.background))

    def __config_game(self):
        self.director.push_scene(InGameConfigurationMenu(self.background))

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
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 100),
        )

        self.go_back_button = self.__create_button("Resume", self.__resume_game, -120)
        self.buttons.append(self.go_back_button)
        self.buttons.append(
            self.__create_button("Configuration", self.__config_game, -40)
        )
        self.buttons.append(
            self.__create_button("Return to menu", self.__return_to_menu, 40)
        )
        self.buttons.append(self.__create_button("Quit game", self.__quit_game, 120))

        self.gui_group.add(self.title, self.buttons)
        super().setup()
