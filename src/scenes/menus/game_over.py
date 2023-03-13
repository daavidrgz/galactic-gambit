from scenes.menus.vertical_menu import VerticalMenu


class GameOver(VerticalMenu):
    def __init__(self):
        super().__init__()
        self.add_button("Retry", self.__retry)
        self.add_button("Main Menu", self.__main_menu)

    def __retry(self):
        self.director.pop_scene()

    def __main_menu(self):
        self.director.pop_scene()
        self.director.pop_scene()

    def setup(self):
        super().setup()
        self.set_title("Game Over")
