import pygame

from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from gui.components.text_button import TextButton
from gui.components.title import Title
from scenes.levels.planet.planet_level import PlanetLevel
from scenes.levels.ship.ship_level import ShipLevel
from scenes.menus.configuration_menu import ConfigurationMenu
from scenes.menus.vertical_menu import VerticalMenu
from scenes.transition import Transition
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

        self.scene_music = Resource.START_MENU_MUSIC

    def __new_game(self):
        next_level = ShipLevel
        self.game_model.level = next_level
        self.game_model.save()
        self.director.push_scene(Transition(next_level()))

    def __continue_game(self):
        self.game_model.load()
        current_level = self.game_model.get_level()
        self.director.push_scene(Transition(current_level()))

    def __leave_game(self):
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

    def __get_offsets(self):
        if self.game_model.save_exists():
            return [-50, 50, 150]
        else:
            return [-100, 0, 100]

    def setup(self):
        self.__generate_gui()
        super().setup()

    def __generate_gui(self):
        self.title = Title(
            text="Space Mission",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH / 2, 100),
        )
        if self.game_model.save_exists():
            self.buttons.append(
                self.__create_button("Continue Game", self.__continue_game, -150)
            )

        offsets = self.__get_offsets()
        self.buttons.append(
            self.__create_button("New Game", self.__new_game, offsets[0])
        )
        self.buttons.append(
            self.__create_button("Configuration", self.__config_game, offsets[1])
        )
        self.buttons.append(
            self.__create_button("Quit Game", self.__leave_game, offsets[2])
        )

        self.gui_group.add(self.title, self.buttons)

    def pop_back(self):
        self.gui_group.empty()
        self.buttons = []
        self.__generate_gui()
        self.buttons[self.current_button].select()
        super().pop_back()
