from gui.components.buttons.text_button import TextButton


class SeedButton(TextButton):
    MAX_SEED_LENGTH = 10

    def __init__(
        self,
        seed,
        font,
        color,
        color_hover,
        action,
        position,
    ):
        self.seed = seed
        self.previous_color = color

        full_text = self.__get_full_text()
        super().__init__(
            text=full_text,
            font=font,
            color=color,
            color_hover=color_hover,
            action=lambda: self.__action(action),
            position=position,
        )

    def __get_full_text(self):
        return f"Seed: {self.seed}"

    def __action(self, action):
        self.previous_color = self.current_color
        self.set_color((255, 255, 0))
        action()

    def remove_last_char(self):
        self.seed = self.seed[:-1]
        self.set_text(self.__get_full_text())

    def add_char(self, char):
        if len(self.seed) >= self.MAX_SEED_LENGTH:
            return
        self.seed += char
        self.set_text(self.__get_full_text())

    def reset_color(self):
        self.set_color(self.previous_color)
