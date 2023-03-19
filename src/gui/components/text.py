from gui.components.base_gui import BaseGui


class Text(BaseGui):
    def __init__(self, text, font, color, position):
        self.text = text
        self.font = font
        self.color = color

        text_surface = self.font.render(text, True, color)
        super().__init__(text_surface, position)
