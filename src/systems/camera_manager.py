from utils.singleton import Singleton
from entities.entity import Entity

import pygame
import numpy as np
from constants import DESIGN_WIDTH, DESIGN_HEIGHT, DESIGN_FRAMERATE, CAMERA_LAG_BEHIND

class CameraManager(metaclass=Singleton):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0

    def update(self, elapsed_time):
        direction = np.array([self.target_x - self.x, self.target_y - self.y], dtype=np.float64)
        direction *= elapsed_time * DESIGN_FRAMERATE / 1000.0 / CAMERA_LAG_BEHIND

        if np.linalg.norm(direction) < 0.2: direction = np.zeros(2)

        self.x = self.x + direction[0]
        self.y = self.y + direction[1]

    def set_coords(self, coords):
        self.x, self.y = coords

    def get_coords(self):
        return self.x, self.y

    def set_center(self, coords):
        self.x = coords[0] - DESIGN_WIDTH // 2
        self.y = coords[1] - DESIGN_HEIGHT // 2

    def get_center(self):
        return (
            self.x + DESIGN_WIDTH // 2,
            self.y + DESIGN_HEIGHT // 2
        )

    def set_target_center(self, coords):
        self.target_x = coords[0] - DESIGN_WIDTH // 2
        self.target_y = coords[1] - DESIGN_HEIGHT // 2

class ScrollableGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        self.camera_mgr = CameraManager()
        super().__init__(sprites)

    def draw(self, surface):
        scrollx, scrolly = self.camera_mgr.get_coords()
        sprites = self.sprites()

        def calculate_rect(entity: Entity):
            copy = entity.image_rect.copy()
            copy.centerx = entity.x - scrollx
            copy.centery = entity.y - scrolly
            return copy

        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, calculate_rect(spr)) for spr in sprites if abs(spr.x - (scrollx + DESIGN_WIDTH // 2)) < DESIGN_WIDTH // 1.8 and abs(spr.y - (scrolly + DESIGN_HEIGHT // 2)) < DESIGN_HEIGHT // 1.8),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, calculate_rect(spr))
                
        self.lostsprites = []
        return self.lostsprites