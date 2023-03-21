from gui.components.text import Text


class BlinkText(Text):
    def __init__(self, text, font, color, position, blink_time, only_once=False):
        super().__init__(text, font, color, position)
        self.blink_time = blink_time
        self.__current_time = 0
        self.image.set_alpha(0)
        self.only_once = only_once
        self.is_visible = False

    def update(self, elapsed_time):
        if self.is_visible and self.only_once:
            return
        self.__current_time += elapsed_time
        if self.__current_time > self.blink_time:
            self.__current_time = 0
            self.image.set_alpha(0 if self.is_visible else 255)
            self.is_visible = not self.is_visible

        super().update(elapsed_time)
