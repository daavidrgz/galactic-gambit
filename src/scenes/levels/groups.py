import pygame
from constants.game_constants import (
    DESIGN_HEIGHT,
    DESIGN_WIDTH,
    SCROLL_CLIPPING_LENIANCY,
)

from systems.camera_manager import CameraManager


class ScrollableGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        self.camera_mgr = CameraManager()
        self.parallax_x = self.parallax_y = 1.0
        self.cull = True
        super().__init__(sprites)

    def draw(self, surface):
        scrollx, scrolly = self.camera_mgr.get_coords()
        sprites = self.sprites()

        def calculate_rect(entity):
            copy = entity.image_rect.copy()
            copy.centerx = round(entity.x) - round(scrollx * self.parallax_x)
            copy.centery = round(entity.y) - round(scrolly * self.parallax_y)
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
                        if abs(spr.x - (scrollx + half_width)) < width_clip
                        and abs(spr.y - (scrolly + half_height)) < height_clip
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
