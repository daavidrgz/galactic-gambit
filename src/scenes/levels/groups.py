import pygame
from constants.game_constants import (
    DESIGN_HEIGHT,
    DESIGN_WIDTH,
    SCROLL_CLIPPING_LENIANCY,
)

from systems.camera_manager import CameraManager
from utils.observable import Observable


class ScrollableGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        self.camera_mgr = CameraManager.get_instance()
        self.parallax_x = self.parallax_y = 1.0
        self.cull = True
        super().__init__(sprites)

    def draw(self, surface):
        scrollx, scrolly = self.camera_mgr.get_coords()
        sprites = self.sprites()

        def calculate_rect(entity):
            copy = entity.rect.copy()
            copy.centerx = round(entity.position[0]) - round(scrollx * self.parallax_x)
            copy.centery = round(entity.position[1]) - round(scrolly * self.parallax_y)
            return copy

        if hasattr(surface, "blits"):
            half_width = DESIGN_WIDTH // 2
            half_height = DESIGN_HEIGHT // 2
            width_clip = DESIGN_WIDTH // (2 - SCROLL_CLIPPING_LENIANCY)
            height_clip = DESIGN_HEIGHT // (2 - SCROLL_CLIPPING_LENIANCY)
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (spr.image, calculate_rect(spr))
                        for spr in sprites
                        if abs(spr.position[0] - (scrollx + half_width)) < width_clip
                        and abs(spr.position[1] - (scrolly + half_height)) < height_clip
                    )
                    if self.cull
                    else surface.blits(
                        (spr.image, calculate_rect(spr)) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, calculate_rect(spr))

        self.lostsprites = []
        return self.lostsprites


class ParallaxGroup(ScrollableGroup):
    def __init__(self, parallax, *sprites):
        super().__init__(*sprites)
        self.parallax_x, self.parallax_y = parallax
        self.cull = False


class EnemyGroup(ScrollableGroup, Observable):
    def __init__(self, *sprites):
        self.num_sprites = 0
        Observable.__init__(self)
        super().__init__(sprites)

    def add_internal(self, sprite):
        super().add_internal(sprite)
        self.num_sprites += 1
        self.notify_listeners(self)

    def remove_internal(self, sprite):
        super().remove_internal(sprite)
        self.num_sprites -= 1
        self.notify_listeners(self)

    def empty(self):
        super().empty()
        self.num_sprites = 0
        self.notify_listeners(self)

    def get_num_enemies(self):
        return self.num_sprites
