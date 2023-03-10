import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.text_button import TextButton
from gui.title import Title
from gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.configuration_menu import ConfigurationMenu
from scenes.menus.vertical_menu import VerticalMenu
from scenes.test_level import TestLevel
from systems.resource_manager import Resource


class StartMenu(VerticalMenu):
    def __init__(self):
        super().__init__()
        background_image = self.resource_manager.load_image(Resource.SPACE_BACKGROUND)
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

    def __new_game(self):
        self.director.push_scene(TestLevel())

    def __continue_game(self):
        current_level = self.game_model.get_level()
        self.director.push_scene(current_level())

    def __leave_game(self):
        self.director.leave_game()

    def __config_game(self):
        self.director.push_scene(ConfigurationMenu(self.background))

    def setup(self):
        font = self.resource_manager.load_font(Resource.FONT_LG)

        self.title = Title(
            text="Space Mission",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 100),
        )

        self.continue_game_button = TextButton(
            text="Continue Game",
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__continue_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.new_game_button = TextButton(
            text="New Game",
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__new_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.config_game_button = TextButton(
            text="Configuration",
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__config_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.quit_game_button = TextButton(
            text="Quit Game",
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__leave_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        if self.game_model.save_exists():
            self.buttons.append(self.continue_game_button)

            self.continue_game_button.set_position_rel((0, -150))
            self.new_game_button.set_position_rel((0, -50))
            self.config_game_button.set_position_rel((0, 50))
            self.quit_game_button.set_position_rel((0, 150))
        else:
            self.new_game_button.set_position_rel((0, -100))
            self.quit_game_button.set_position_rel((0, 100))

        self.buttons.append(self.new_game_button)
        self.buttons.append(self.config_game_button)
        self.buttons.append(self.quit_game_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()
