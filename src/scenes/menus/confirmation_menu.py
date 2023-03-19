from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from constants.gui_constants import COLOR_BRIGHT, COLOR_SUBTLE
from gui.components.buttons.text_button import TextButton
from gui.components.title import Title
from scenes.menus.horizontal_menu import HorizontalMenu
from systems.resource_manager import Resource


class ConfirmationMenu(HorizontalMenu):
    def __init__(self, confirm_action, background):
        super().__init__()
        self.confirm_action = confirm_action
        self.background = background

    def __create_button(self, text, action, offset):
        font = self.resource_manager.load_font(Resource.FONT_LG)
        return TextButton(
            text=text,
            font=font,
            color=COLOR_SUBTLE,
            color_hover=COLOR_BRIGHT,
            action=action,
            position=(DESIGN_WIDTH / 2 + offset, DESIGN_HEIGHT / 2),
        )

    def __confirm(self):
        self.director.pop_scene()
        self.confirm_action()

    def __go_back(self):
        self.director.pop_scene()

    def setup(self):
        self.title = Title(
            text="Are you sure?",
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.go_back_button = self.__create_button("No", self.__go_back, -100)
        self.go_back_button.confirm_sound = Resource.GO_BACK_SOUND
        self.buttons.append(self.go_back_button)

        confirm_button = self.__create_button("Yes", self.__confirm, 100)
        confirm_button.confirm_sound = Resource.GO_BACK_ALT_SOUND
        self.buttons.append(confirm_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()
