from gui.components.buttons.action_button import ActionButton


class SeedButton(ActionButton):
    MAX_SEED_LENGTH = 9

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
        return f"Seed: {self.seed}"

    def remove_last_char(self):
        self.seed = self.seed[:-1]
        self.set_text(self.__get_full_text())

    def add_char(self, char):
        if len(self.seed) >= self.MAX_SEED_LENGTH:
            return
        self.seed += char
        self.set_text(self.__get_full_text())

    def set_seed(self, seed):
        self.seed = seed
        self.set_text(self.__get_full_text())

    def empty_seed(self):
        self.seed = ""
        self.set_text(self.__get_full_text())
