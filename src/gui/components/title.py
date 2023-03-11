from gui.components.base_gui import BaseGui


class Title(BaseGui):
    def __init__(self, text, font, color, position):
        self.text = text
        self.font = font
        self.color = color

        self.font.set_bold(True)
        self.image = self.font.render(text, True, color)
        super().__init__(self.image, position)
