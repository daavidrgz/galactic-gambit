import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.button import Button
from gui.components.buttons.seed_button import SeedButton
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
        self.is_changing_seed = False

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

    def __change_seed(self):
        self.disable_mouse = True
        self.is_changing_seed = True

    def __go_back(self):
        self.director.pop_scene()

    def setup(self):
        font = self.resource_manager.load_font(Resource.FONT_LG)

        self.title = Title(
            text="Configuration",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.buttons.append(self.__create_button("Volume", self.__volume_config, -120))
        self.buttons.append(
            self.__create_button("Keybindings", self.__keybindings_config, -40)
        )

        seed_button = SeedButton(
            seed="14923",
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__change_seed,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 + 40),
        )
        self.buttons.append(seed_button)
        go_back_button = self.__create_button("Go back", self.__go_back, 120)
        go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        if not self.is_changing_seed:
            super().handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.disable_mouse = False
                    self.get_selected_button().reset_color()
                    self.is_changing_seed = False
                    return
                if event.key == pygame.K_BACKSPACE:
                    self.get_selected_button().remove_last_char()
                    return
                if event.key == pygame.K_SPACE:
                    return
                if event.unicode.isnumeric():
                    self.get_selected_button().add_char(event.unicode)
