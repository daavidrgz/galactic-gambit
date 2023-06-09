import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.buttons.text_button import TextButton
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from gui.components.buttons.rebind_button import RebindButton
from gui.components.title import Title
from scenes.menus.vertical_menu import VerticalMenu
from systems.control_system import Action
from systems.resource_manager import Resource


class KeybindingsMenu(VerticalMenu):
    def __init__(self, background, subtle, bright):
        super().__init__()
        self.background = background
        self.is_changing_keybind = False
        self.subtle = subtle
        self.bright = bright

    def __change_keybind(self):
        self.disable_mouse = True
        self.is_changing_keybind = True

    def __go_back(self):
        self.director.pop_scene()

    def update(self, elapsed_time):
        super().update(elapsed_time)
        if not self.is_changing_keybind:
            return

    def __create_button(self, text, action, offset):
        font = self.resource_manager.load_font(Resource.FONT_MD)
        return RebindButton(
            action_text=text,
            bind_action=action,
            bind_key=self.control_system.get_action_key(action),
            font=font,
            color=self.subtle,
            color_hover=self.bright,
            action=self.__change_keybind,
            position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 + offset),
        )

    def setup(self):
        self.title = Title(
            text="Keybindings",
            color=self.bright,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.buttons.append(self.__create_button("Move Up", Action.UP, -100))
        self.buttons.append(self.__create_button("Move Left", Action.LEFT, -50))
        self.buttons.append(self.__create_button("Move Down", Action.DOWN, 0))
        self.buttons.append(self.__create_button("Move Right", Action.RIGHT, 50))

        self.go_back_button = TextButton(
            text="Go back",
            font=self.resource_manager.load_font(Resource.FONT_MD),
            color=self.subtle,
            color_hover=self.bright,
            action=self.__go_back,
            position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 + 100),
        )
        self.go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(self.go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        if not self.is_changing_keybind:
            super().handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.is_changing_keybind = False
                self.disable_mouse = False
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.get_selected_button().reset_color()
                    return
                self.get_selected_button().rebind_action(event.key)
