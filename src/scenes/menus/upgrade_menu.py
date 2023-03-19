import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.components.title import Title
from gui.components.upgrade_card import UpgradeCard
from constants.gui_constants import COLOR_BRIGHT
from scenes.menus.horizontal_menu import HorizontalMenu
from systems.resource_manager import Resource


class UpgradeMenu(HorizontalMenu):
    def __init__(self, upgrades, apply_upgrade):
        super().__init__()
        background = self.director.virtual_screen.copy()
        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(220)
        background.blit(veil, (0, 0))
        self.background = background
        self.upgrades = upgrades
        self.apply_upgrade = apply_upgrade

    def __create_upgrade_card(self, title, icon, action, offset):
        return UpgradeCard(
            title=title,
            icon=icon,
            position=(DESIGN_WIDTH // 2 + offset, DESIGN_HEIGHT // 2 + 20),
            width=250,
            height=340,
            action=action,
        )

    def __select_upgrade(self, upgrade):
        self.apply_upgrade(upgrade)
        self.director.pop_scene()

    def __get_offsets(self):
        if len(self.upgrades) == 3:
            return [-300, 0, 300]
        elif len(self.upgrades) == 2:
            return [-140, 140]
        elif len(self.upgrades) == 1:
            return [0]

    def setup(self):
        self.title = Title(
            text="Choose your upgrade!",
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        offsets = self.__get_offsets()
        for i, upgrade in enumerate(self.upgrades):
            self.buttons.append(
                self.__create_upgrade_card(
                    title=upgrade.name,
                    icon=self.resource_manager.load_image(upgrade.icon),
                    action=lambda up=upgrade: self.__select_upgrade(up),
                    offset=offsets[i],
                )
            )

        self.gui_group.add(self.title, self.buttons)
        super().setup()
