from gui.components.buttons.text_button import TextButton


class FullScreenButton(TextButton):
    def __init__(self, full_screen, font, color, color_hover, action, position):
        self.full_screen = full_screen
        full_text = self.__get_full_text()
        super().__init__(
            text=full_text,
            font=font,
            color=color,
            color_hover=color_hover,
            action=action,
            position=position,
        )

    def __get_full_text(self):
        return f"Full Screen: " + ("ON" if self.full_screen else "OFF")

    def toggle_full_screen(self):
        self.full_screen = not self.full_screen
        self.set_text(self.__get_full_text())
