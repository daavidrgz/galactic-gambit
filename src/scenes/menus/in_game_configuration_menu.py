import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.full_screen_button import FullScreenButton
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.keybinds_menu import KeybindingsMenu
from scenes.menus.vertical_menu import VerticalMenu
from scenes.menus.volume_menu import VolumeMenu
from systems.resource_manager import Resource


class InGameConfigurationMenu(VerticalMenu):
    def __init__(self, background):
        super().__init__()
        self.background = background

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

    def __keybindings_config(self):
        self.director.push_scene(KeybindingsMenu(self.background, COLOR_SUBTLE, COLOR_BRIGHT))

    def __volume_config(self):
        self.director.push_scene(VolumeMenu(COLOR_SUBTLE, COLOR_BRIGHT, self.background))

    def __toggle_full_screen(self):
        self.get_selected_button().toggle_full_screen()
        self.director.toggle_full_screen()

    def __go_back(self):
        self.director.pop_scene()

    def setup(self):
        self.title = Title(
            text="Configuration",
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        full_screen_button = FullScreenButton(
            full_screen=self.director.full_screen,
            font=self.resource_manager.load_font(Resource.FONT_LG),
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__toggle_full_screen,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 - 120),
        )
        self.buttons.append(full_screen_button)

        self.buttons.append(self.__create_button("Volume", self.__volume_config, -40))
        self.buttons.append(
            self.__create_button("Keybindings", self.__keybindings_config, 40)
        )

        self.go_back_button = self.__create_button("Go back", self.__go_back, 120)
        self.go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(self.go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()
