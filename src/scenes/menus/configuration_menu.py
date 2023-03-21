import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.full_screen_button import FullScreenButton
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
        self.director.push_scene(
            KeybindingsMenu(self.background, COLOR_SUBTLE, COLOR_BRIGHT)
        )

    def __volume_config(self):
        self.director.push_scene(
            VolumeMenu(COLOR_SUBTLE, COLOR_BRIGHT, self.background)
        )

    def __change_seed(self):
        self.disable_mouse = True
        self.get_selected_button().empty_seed()
        self.is_changing_seed = True

    def __toggle_full_screen(self):
        self.get_selected_button().toggle_full_screen()
        self.director.toggle_full_screen()

    def __go_back(self):
        self.director.pop_scene()

    def setup(self):
        font = self.resource_manager.load_font(Resource.FONT_LG)

        self.title = Title(
            text="Configuration",
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        full_screen_button = FullScreenButton(
            full_screen=self.director.full_screen,
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__toggle_full_screen,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 - 120),
        )
        self.buttons.append(full_screen_button)
        self.buttons.append(self.__create_button("Volume", self.__volume_config, -40))
        self.buttons.append(
            self.__create_button("Keybindings", self.__keybindings_config, +40)
        )

        current_seed = self.rng_system.get_seed()
        seed_button = SeedButton(
            seed=str(current_seed),
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__change_seed,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2 + 120),
        )
        self.buttons.append(seed_button)
        self.go_back_button = self.__create_button("Go back", self.__go_back, 200)
        self.go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(self.go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        if not self.is_changing_seed:
            super().handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.disable_mouse = False
                    self.get_selected_button().reset_color()
                    self.is_changing_seed = False
                    self.rng_system.seed(int(self.get_selected_button().seed))
                    self.get_selected_button().set_seed(str(self.rng_system.get_seed()))
                    return
                if event.key == pygame.K_ESCAPE:
                    # If escape is pressed, do not save seed changes
                    self.disable_mouse = False
                    self.get_selected_button().reset_color()
                    self.get_selected_button().set_seed(str(self.rng_system.get_seed()))
                    self.is_changing_seed = False
                    return
                if event.key == pygame.K_BACKSPACE:
                    self.get_selected_button().remove_last_char()
                    return
                if event.key == pygame.K_SPACE:
                    return
                if event.unicode.isnumeric():
                    self.get_selected_button().add_char(event.unicode)
