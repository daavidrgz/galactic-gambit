import pygame
from scenes.scene import Scene
from scenes.scroll import Scroll


class ScrollableScene(Scene):
    def __init__(self):
        super().__init__()
        self.all_sprites = pygame.sprite.Group()
        self.scroll = Scroll((0, 0))
        # Force first update in order to be consistent with scroll
        self.is_scroll_modified = True

    def update_sprites_relative_position(self):
        if self.is_scroll_modified:
            for sprite in self.all_sprites:
                sprite.update_relative_position(self.scroll)
            self.is_scroll_modified = False
