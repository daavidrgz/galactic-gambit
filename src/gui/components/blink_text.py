from gui.components.text import Text


class BlinkText(Text):
    def __init__(self, text, font, color, position, blink_time):
        super().__init__(text, font, color, position)
        self.blink_time = blink_time
        self.current_time = 0
        self.image.set_alpha(0)

    def update(self, elapsed_time):
        self.current_time += elapsed_time
        if self.current_time > self.blink_time:
            self.current_time = 0
            self.image.set_alpha(0 if self.image.get_alpha() == 255 else 255)

        super().update(elapsed_time)
