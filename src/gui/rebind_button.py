import pygame
from gui.button import Button
from systems.control_system import ControlSystem


class RebindButton(Button):
    def __init__(
        self,
        action_text,
        bind_action,
        bind_key,
        font,
        color,
        color_hover,
        action,
        position,
    ):
        self.control_system = ControlSystem.get_instance()
        self.action_text = action_text
        self.bind_action = bind_action
        self.bind_key = bind_key
        self.previous_color = color

        full_text = self.__get_full_text(bind_key)
        super().__init__(full_text, font, color, color_hover, action, position)

    def __get_full_text(self, bind_key):
        key_name = pygame.key.name(bind_key)
        return f"{self.action_text} - {key_name}"

    def execute_action(self):
        self.previous_color = self.current_color
        self.set_color((255, 255, 0))
        super().execute_action()

    def reset_color(self):
        self.set_color(self.previous_color)

    def rebind_action(self, bind_key):
        self.control_system.rebind_action(self.bind_action, bind_key)
        self.bind_key = bind_key
        self.set_text(self.__get_full_text(bind_key))
        self.reset_color()
