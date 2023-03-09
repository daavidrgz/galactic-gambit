import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.button import Button
from gui.title import Title
from gui.volume_button import VolumeButton
from gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from scenes.menus.menu import Menu
from systems.resource_manager import Resource
from systems.sound_controller import SoundController


class VolumeMenu(Menu):
    def __init__(self, background=pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))):
        super().__init__()
        self.sound_controller = SoundController.get_instance()
        self.background = background
        self.is_changing_volume = False

    def __change_volume_state(self):
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
                position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 - 100),
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

        self.go_back_button = Button(
            text="Go back",
            font=self.resource_manager.load_font(Resource.FONT_LG),
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=self.__go_back,
            position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 + 100),
        )
        self.buttons.append(self.go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        if not self.is_changing_volume:
            super().handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.get_selected_button().reset_color()
                    self.is_changing_volume = False
                    return

                if event.key == pygame.K_UP:
                    self.get_selected_button().increase_volume()
                    return

                if event.key == pygame.K_DOWN:
                    self.get_selected_button().decrease_volume()
                    return
