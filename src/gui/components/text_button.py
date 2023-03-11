from gui.components.button import Button


class TextButton(Button):
    def __init__(
        self,
        text,
        font,
        color,
        color_hover,
        action,
        position,
        background=None,
        background_hover=None,
    ):
        self.text = text
        self.font = font
        self.color = color
        self.color_hover = color_hover
        self.background = background
        self.background_hover = background_hover

        self.current_background = background
        self.current_color = color

        self.text_surface = self.__render_font(text, color, background)

        super().__init__(
            surface=self.text_surface,
            position=position,
            action=action,
            on_select=lambda: self.set_color(self.color_hover),
            on_deselect=lambda: self.set_color(self.color),
        )

    def __render_font(self, text, color, background):
        return self.font.render(text, True, color, background)

    def set_text(self, text):
        self.text = text
        self.image = self.__render_font(
            text, self.current_color, self.current_background
        )

    def set_color(self, color):
        self.current_color = color
        self.image = self.__render_font(self.text, color, self.background)

    def set_background(self, background):
        self.current_background = background
        self.image = self.__render_font(self.text, self.current_color, background)
