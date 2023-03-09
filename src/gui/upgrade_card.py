import pygame
from gui.button import Button
from gui_constants import COLOR_BRIGHT
from systems.resource_manager import Resource, ResourceManager


class UpgradeCard(Button):
    def __init__(self, title, icons, description, position, width, height, action):
        self.resource_manager = ResourceManager.get_instance()
        self.title = title
        self.icons = icons
        self.description = description
        self.width = width
        self.height = height

        self.card = pygame.Surface((width, height))
        self.card.fill((0, 0, 0))
        title_surface = self.__get_title(title)
        self.card.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 25))

        super().__init__(
            surface=self.card,
            position=position,
            action=action,
            on_select=self.on_select,
            on_deselect=self.on_deselect,
        )

    def on_select(self):
        pass

    def on_deselect(self):
        pass

    def __get_title(self, title):
        font = self.resource_manager.load_font(Resource.FONT_MD)
        return font.render(title, True, COLOR_BRIGHT)
