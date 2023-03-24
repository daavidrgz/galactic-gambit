from gui.components.buttons.button import Button


class TextButton(Button):
    def __init__(
        self,
        text,
        font,
        color,
        color_hover,
        action,
        position,
    ):
        self.text = text
        self.font = font
        self.color = color
        self.color_hover = color_hover

        self.current_color = color

        self.text_surface = self.__render_font(text, color)

        super().__init__(
            surface=self.text_surface,
            position=position,
            action=action,
            on_select=lambda: self.set_color(self.color_hover),
            on_deselect=lambda: self.set_color(self.color),
        )

    def __render_font(self, text, color):
        return self.font.render(text, True, color)

    def set_text(self, text):
        self.text = text
        self.set_surface(
            self.__render_font(text, self.current_color)
        )

    def set_color(self, color):
        self.current_color = color
        self.set_surface(self.__render_font(self.text, color))
