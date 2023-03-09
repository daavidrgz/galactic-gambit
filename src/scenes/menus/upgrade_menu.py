from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.title import Title
from gui.upgrade_card import UpgradeCard
from gui_constants import COLOR_BRIGHT
from scenes.menus.horizontal_menu import HorizontalMenu
from systems.resource_manager import Resource


class UpgradeMenu(HorizontalMenu):
    def __init__(self, background):
        super().__init__()
        self.background = background

    def __create_upgrade_card(self, title, icon, action, offset):
        return UpgradeCard(
            title=title,
            icon=icon,
            position=(DESIGN_WIDTH // 2 + offset, DESIGN_HEIGHT // 2 + 20),
            width=200,
            height=320,
            action=action,
        )

    def __action(self):
        print("Upgrade chosen")

    def setup(self):
        self.title = Title(
            text="Choose your upgrade!",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.buttons.append(
            self.__create_upgrade_card(
                title="Woobly Bullet",
                icon=self.resource_manager.load_image(Resource.PLAYER),
                action=self.__action,
                offset=-240,
            )
        )
        self.buttons.append(
            self.__create_upgrade_card(
                title="First Upgrade",
                icon=self.resource_manager.load_image(Resource.PLAYER),
                action=self.__action,
                offset=0,
            )
        )
        self.buttons.append(
            self.__create_upgrade_card(
                title="First Upgrade",
                icon=self.resource_manager.load_image(Resource.PLAYER),
                action=self.__action,
                offset=240,
            )
        )

        self.gui_group.add(self.title, self.buttons)
        super().setup()
