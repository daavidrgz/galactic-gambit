import numpy as np
from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from systems.resource_manager import Resource, ResourceManager

import pygame

class PlanetTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = []

        for x in range(85 - 15, 85 + 16):
            for y in range(85 - 15, 85 + 16):
                distance_sqr = (x // 2 * 2 - 85) ** 2 + (y // 2 * 2 - 85) ** 2
                if distance_sqr < 11**2:
                    self.data[y, x] = TerrainType.GROUND
                elif distance_sqr < 12**2:
                    self.starting_tiles.append((x, y))

        for x, y in [(81,84),(81,83),(81,82),
                     (82,84),(82,83),(82,82),
                     (83,84),(83,83),(83,82),
                     (84,84),(84,83),(85,84),
                     (85,83)]:
            self.data[y, x] = TerrainType.WALL

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 85.5)

        self.place_start_sprite(82, 84)

    def place_end(self, end_pos):
        for x in range(end_pos[0] - 7, end_pos[0] + 8):
            for y in range(end_pos[1] - 7, end_pos[1] + 8):
                distance_sqr = (x // 2 * 2 - end_pos[0]) ** 2 + (
                    y // 2 * 2 - end_pos[1]
                ) ** 2
                if distance_sqr < 5**2:
                    self.data[y, x] = TerrainType.GROUND

        self.data[
            end_pos[1] : end_pos[1] + 2, end_pos[0] : end_pos[0] + 2
        ] = TerrainType.WALL
        self.end_position = (
            (end_pos[0] + 0.5) * TILE_SIZE,
            (end_pos[1] + 0.5) * TILE_SIZE,
        )

    def place_start_sprite(self, x, y):
        init_room_spr = pygame.sprite.Sprite()
        init_room_spr.image = ResourceManager().load_image(Resource.PLANET_START)
        init_room_spr.rect = init_room_spr.image.get_rect()
        init_room_spr.rect.topleft = (
            (x - 1) * TILE_SIZE,
            (y - 2) * TILE_SIZE,
        )
        self.sprites_top.add(init_room_spr)
