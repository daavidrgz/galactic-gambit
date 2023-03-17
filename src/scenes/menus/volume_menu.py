import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from gui.components.buttons.volume_button import VolumeButton
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.vertical_menu import VerticalMenu
from systems.resource_manager import Resource


class VolumeMenu(VerticalMenu):
    def __init__(self, background=pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))):
        super().__init__()
        self.background = background
        self.is_changing_volume = False
        self.input_timeout = 50
        self.current_timeout = 0

    def __change_volume_state(self):
        self.disable_mouse = True
        self.is_changing_volume = True

    def __go_back(self):
        self.director.pop_scene()

    def setup(self):
        font = self.resource_manager.load_font(Resource.FONT_LG)

        self.title = Title(
            text="Volume",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.buttons.append(
            VolumeButton(
                volume_text="FX volume",
                volume_level=self.sound_controller.get_effects_volume(),
                increase_volume_cb=self.sound_controller.increase_effects_volume,
                decrease_volume_cb=self.sound_controller.decrease_effects_volume,
                action=self.__change_volume_state,
                position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 - 80),
                font=font,
                color=COLOR_SUBTLE,
                color_hover=COLOR_BRIGHT,
            )
        )

        self.buttons.append(
            VolumeButton(
                volume_text="Music volume",
                volume_level=self.sound_controller.get_music_volume(),
                increase_volume_cb=self.sound_controller.increase_music_volume,
                decrease_volume_cb=self.sound_controller.decrease_music_volume,
                action=self.__change_volume_state,
                position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2),
                font=font,
                color=COLOR_SUBTLE,
                color_hover=COLOR_BRIGHT,
            )
        )

        go_back_button = TextButton(
            text="Go back",
            font=self.resource_manager.load_font(Resource.FONT_LG),
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__go_back,
            position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 + 80),
        )
        go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def __volume_change_ready(self):
        return self.current_timeout >= self.input_timeout

    def __update_timeout(self, elapsed_time):
        self.current_timeout = self.current_timeout + elapsed_time

    def update(self, elapsed_time):
        if self.is_changing_volume:
            self.__update_timeout(elapsed_time)
        super().update(elapsed_time)

    def handle_events(self, events):
        if not self.is_changing_volume:
            super().handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.disable_mouse = False
                    self.get_selected_button().reset_color()
                    self.current_timeout = 0
                    self.is_changing_volume = False
                    return

        if not self.__volume_change_ready():
            return

        self.current_timeout = 0
        if self.control_system.is_key_pressed(pygame.K_UP):
            self.get_selected_button().increase_volume()

        if self.control_system.is_key_pressed(pygame.K_DOWN):
            self.get_selected_button().decrease_volume()
