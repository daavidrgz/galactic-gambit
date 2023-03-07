from scenes.level import Level
from generation.tile import Tile
from scenes.director import Director
from generation.generator import BaseGenerator
from systems.camera_manager import ParallaxGroup
from systems.resource_manager import ResourceManager
from generation.base_terrain import BaseTerrain, TerrainType

from noise import snoise2
import numpy as np
import pygame

from constants import TILE_SIZE

class CaveGenerator(BaseGenerator):
    def __init__(self, terrain):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = self.resource_manager.load_tile(self.resource_manager.DIRT)
        self.cobble_sprite = self.resource_manager.load_tile(
            self.resource_manager.COBBLESTONE
        )

        super().__init__(
            (6.0, 6.0),
            (2, 4),
            terrain
        )

    def coordinate_transform(self, x, y):
        return (x + snoise2(x * 10.0, y * 10.0) * y / 40, y + snoise2(x * 10.0, y * 10.0) * y / 40)

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        return self.dirt_sprite
    
    def noise_wall_condition(self, n, x, y):
        return n > 0.0

class CaveTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = [(84, 3), (85, 3), (86, 3)]

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(resource_manager.POLISHED_ANDESITE)
        for x in range(85 - 1, 85 + 2):
            for y in range(0, 3):
                self.data[y, x] = TerrainType.GROUND
                self.sprites.add(Tile(x, y, andesite_sprite))

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 1.5)

class CaveLevel(Level):
    def __init__(self):
        terrain = CaveTerrain()
        generator = CaveGenerator(terrain)
        background_color = (40, 30, 20)

        super().__init__(generator, terrain, background_color)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(CaveLevel())

        super().handle_events(events)