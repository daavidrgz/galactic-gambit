from scenes.level import Level
from generation.tile import Tile
from scenes.director import Director
from generation.generator import BaseGenerator
from systems.camera_manager import ParallaxGroup
from systems.resource_manager import ResourceManager
from generation.base_terrain import BaseTerrain, TerrainType

import numpy as np
import pygame

from constants import TILE_SIZE

class PlanetGenerator(BaseGenerator):
    def __init__(self, terrain):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = self.resource_manager.load_tile(self.resource_manager.DIRT)
        self.cobble_sprite = self.resource_manager.load_tile(
            self.resource_manager.COBBLESTONE
        )

        super().__init__(
            (10.0, 10.0),
            (2, 2),
            terrain
        )

    def coordinate_transform(self, x, y):
        x -= 85
        y -= 85
        return (np.sqrt(x*x + y*y), np.arctan2(y, x) * 5)

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        return self.dirt_sprite
    
    def noise_wall_condition(self, n, x, y):
        return n < (x / 114)**3

class PlanetTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = []

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(resource_manager.POLISHED_ANDESITE)
        for x in range(85 - 15, 85 + 16):
            for y in range(85 - 15, 85 + 16):
                distance_sqr = (x - 85)**2 + (y - 85)**2
                if distance_sqr < 11**2:
                    self.data[y, x] = TerrainType.GROUND
                    self.sprites.add(Tile(x, y, andesite_sprite))
                elif distance_sqr < 12**2:
                    self.starting_tiles.append((x, y))

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 85.5)

class PlanetLevel(Level):
    def __init__(self):
        terrain = PlanetTerrain()
        generator = PlanetGenerator(terrain)
        background_color = (40, 30, 20)

        rmgr = ResourceManager()
        dust_sprite = pygame.sprite.Sprite()
        dust_sprite.image = pygame.transform.smoothscale(rmgr.load_image(rmgr.DIRT), (TILE_SIZE * 100.0, TILE_SIZE * 100.0))
        dust_sprite.image.set_alpha(100)
        dust_sprite.rect = dust_sprite.image.get_rect()
        dust_sprite.image_rect = dust_sprite.image.get_rect()
        dust_sprite.x = dust_sprite.y = TILE_SIZE * 45.5
        self.dust = ParallaxGroup((0.5, 0.5), dust_sprite)

        super().__init__(generator, terrain, background_color)

    def draw(self, screen):
        super().draw(screen)
        self.dust.draw(screen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(PlanetLevel())

        super().handle_events(events)