from gui.components.base_gui import BaseGui
from systems.resource_manager import Resource
from systems.sound_controller import SoundController


class Button(BaseGui):
    def __init__(
        self,
        surface,
        action,
        on_select,
        on_deselect,
        position,
    ):
        self.sound_controller = SoundController.get_instance()
        self.action = action
        self.on_select = on_select
        self.on_deselect = on_deselect
        self.is_selected = False
        self.select_sound = Resource.SELECT_SOUND
        self.confirm_sound = Resource.CONFIRM_SOUND

        super().__init__(surface, position)

    def execute_action(self):
        self.sound_controller.play_sound(self.confirm_sound)
        self.action()

    def select(self):
        if self.is_selected:
            return
        self.sound_controller.play_sound(self.select_sound, 100)
        self.on_select()
        self.is_selected = True

    def deselect(self):
        if not self.is_selected:
            return
        self.on_deselect()
        self.is_selected = False
