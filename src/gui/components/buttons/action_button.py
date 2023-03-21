from gui.components.buttons.text_button import TextButton


class ActionButton(TextButton):
    def __init__(
        self,
        text,
        font,
        color,
        color_hover,
        action,
        position,
    ):
        self.__previous_color = color

        super().__init__(
            text=text,
            font=font,
            color=color,
            color_hover=color_hover,
            action=lambda: self.__action(action),
            position=position,
        )

    def __action(self, action):
        self.__previous_color = self.current_color
        self.set_color((255, 255, 0))
        action()

    def reset_color(self):
        self.set_color(self.__previous_color)
