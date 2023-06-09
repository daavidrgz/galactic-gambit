import pygame
from gui.components.buttons.action_button import ActionButton
from systems.control_system import ControlSystem


class RebindButton(ActionButton):
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

        full_text = self.__get_full_text(bind_key)
        super().__init__(
            text=full_text,
            font=font,
            color=color,
            color_hover=color_hover,
            action=action,
            position=position,
        )

    def __get_full_text(self, bind_key):
        key_name = pygame.key.name(bind_key)
        return f"{self.action_text} - {key_name}"

    def rebind_action(self, bind_key):
        self.control_system.rebind_action(self.bind_action, bind_key)
        self.bind_key = bind_key
        self.set_text(self.__get_full_text(bind_key))
        self.reset_color()
