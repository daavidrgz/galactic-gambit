import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.button import Button
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.keybinds_menu import KeybindingsMenu
from scenes.menus.vertical_menu import VerticalMenu
from scenes.menus.volume_menu import VolumeMenu
from systems.resource_manager import Resource


class ConfigurationMenu(VerticalMenu):
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
        self.director.push_scene(KeybindingsMenu(self.background))

    def __volume_config(self):
        self.director.push_scene(VolumeMenu(self.background))

    def __go_back(self):
        self.director.pop_scene()

    def setup(self):
        self.title = Title(
            text="Configuration",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.buttons.append(self.__create_button("Volume", self.__volume_config, -100))
        self.buttons.append(
            self.__create_button("Keybindings", self.__keybindings_config, 0)
        )
        go_back_button = self.__create_button("Go back", self.__go_back, 100)
        go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()
