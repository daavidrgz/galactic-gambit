import pygame
from gui.components.buttons.button import Button
from constants.gui_constants import COLOR_BRIGHT, COLOR_STANDARD, TRANSPARENT
from systems.resource_manager import Resource, ResourceManager


class UpgradeCard(Button):
    ICON_SIZE = 90

    def __init__(self, title, icon, position, width, height, action):
        self.resource_manager = ResourceManager.get_instance()
        self.title = title
        self.icon = icon
        self.width = width
        self.height = height

        self.veil_alpha = 100

        self.border_color = TRANSPARENT
        self.border_width = 6

        super().__init__(
            surface=self.__render_card(),
            position=position,
            action=action,
            on_select=self.on_select,
            on_deselect=self.on_deselect,
        )

    def __render_card(self):
        container = pygame.Surface(
            (self.width + self.border_width, self.height + self.border_width)
        )
        container.fill(self.border_color)

        card = pygame.Surface((self.width, self.height))
        card.fill((0, 0, 0))

        title_surface = self.__get_title(self.title)
        card.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 25))

        card.blit(
            self.icon,
            (
                self.width // 2 - self.ICON_SIZE // 2,
                self.height // 2 - self.ICON_SIZE // 2,
            ),
        )

        veil = pygame.Surface((self.width, self.height))
        veil.fill((0, 0, 0))
        veil.set_alpha(self.veil_alpha)
        card.blit(veil, (0, 0))

        container.blit(card, (self.border_width / 2, self.border_width / 2))
        return container

    def on_select(self):
        self.veil_alpha = 0
        self.border_color = COLOR_BRIGHT
        self.image = self.__render_card()

    def on_deselect(self):
        self.veil_alpha = 100
        self.border_color = TRANSPARENT
        self.image = self.__render_card()

    def __get_title(self, title):
        font = self.resource_manager.load_font(Resource.FONT_MD)
        return font.render(title, True, COLOR_BRIGHT)
