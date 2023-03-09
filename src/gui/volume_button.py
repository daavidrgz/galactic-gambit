from gui.text_button import TextButton
from systems.sound_controller import SoundController


class VolumeButton(TextButton):
    def __init__(
        self,
        volume_text,
        volume_level,
        increase_volume_cb,
        decrease_volume_cb,
        font,
        color,
        color_hover,
        action,
        position,
    ):
        self.sound_controller = SoundController.get_instance()
        self.volume_text = volume_text
        self.volume_level = volume_level
        self.increase_volume_cb = increase_volume_cb
        self.decrease_volume_cb = decrease_volume_cb
        self.previous_color = color

        full_text = self.__get_full_text(volume_level)
        super().__init__(
            text=full_text,
            font=font,
            color=color,
            color_hover=color_hover,
            action=lambda: self.__action(action),
            position=position,
        )

    def __action(self, action):
        self.previous_color = self.current_color
        self.set_color((255, 255, 0))
        action()

    def __get_full_text(self, volume_level):
        return f"{self.volume_text} - {volume_level}"

    def reset_color(self):
        self.set_color(self.previous_color)

    def increase_volume(self):
        self.volume_level = self.increase_volume_cb()
        self.set_text(self.__get_full_text(self.volume_level))

    def decrease_volume(self):
        self.volume_level = self.decrease_volume_cb()
        self.set_text(self.__get_full_text(self.volume_level))
