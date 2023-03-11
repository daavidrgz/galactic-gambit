from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.title import Title
from gui.upgrade_card import UpgradeCard
from gui_constants import COLOR_BRIGHT
from scenes.menus.horizontal_menu import HorizontalMenu
from systems.resource_manager import Resource


class UpgradeMenu(HorizontalMenu):
    def __init__(self, background, upgrades, apply_upgrade):
        super().__init__()
        self.background = background
        self.upgrades = upgrades
        self.apply_upgrade = apply_upgrade

    def __create_upgrade_card(self, title, icon, action, offset):
        return UpgradeCard(
            title=title,
            icon=icon,
            position=(DESIGN_WIDTH // 2 + offset, DESIGN_HEIGHT // 2 + 20),
            width=200,
            height=320,
            action=action,
        )

    def __select_upgrade(self, upgrade):
        self.apply_upgrade(upgrade)

    def __get_offsets(self):
        if len(self.upgrades) == 3:
            return -240, 0, 240
        elif len(self.upgrades) == 2:
            return -120, 120
        elif len(self.upgrades) == 1:
            return 0

    def setup(self):
        self.title = Title(
            text="Choose your upgrade!",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        offsets = self.__get_offsets()
        for i, upgrade in enumerate(self.upgrades):
            self.buttons.append(
                self.__create_upgrade_card(
                    title=upgrade.name,
                    icon=self.resource_manager.load_image(Resource.PLAYER),
                    action=lambda: self.__select_upgrade(upgrade),
                    offset=offsets[i],
                )
            )

        self.gui_group.add(self.title, self.buttons)
        super().setup()
