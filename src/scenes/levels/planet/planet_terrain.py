from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from systems.resource_manager import Resource, ResourceManager
from utils.math import vector2

import pygame
import numpy as np


class PlanetTerrain(BaseTerrain):
    X_SIZE = 171
    Y_SIZE = 171

    def populate(self):
        self.data = np.full((self.X_SIZE, self.Y_SIZE), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = []

        # Spawn room is a circle centered relative to the level
        for x in range(85 - 15, 85 + 16):
            for y in range(85 - 15, 85 + 16):
                distance_sqr = (x // 2 * 2 - 85) ** 2 + (y // 2 * 2 - 85) ** 2
                if distance_sqr < 11**2:
                    self.data[y, x] = TerrainType.GROUND
                elif distance_sqr < 12**2:
                    self.starting_tiles.append((x, y))

        # Collision for crashed ship
        for x, y in [
            (81, 84),
            (81, 83),
            (81, 82),
            (82, 84),
            (82, 83),
            (82, 82),
            (83, 84),
            (83, 83),
            (84, 84),
            (84, 83),
            (85, 84),
            (85, 83),
        ]:
            self.data[y, x] = TerrainType.WALL
        self.place_start_sprite(81, 82)

        self.player_starting_position = vector2(TILE_SIZE * 85.5, TILE_SIZE * 85.5)

    def place_end(self, end_pos):
        # Ensure the end doesn't go out of bounds
        end_pos = (
            np.clip(end_pos[0], 8, self.X_SIZE - 10),
            np.clip(end_pos[1], 8, self.Y_SIZE - 10),
        )

        # Make a small open area for the cave entrance
        for x in range(end_pos[0] - 7, end_pos[0] + 8):
            for y in range(end_pos[1] - 7, end_pos[1] + 8):
                x_dist = (x // 2 * 2 - end_pos[0])**2
                y_dist = (y // 2 * 2 - end_pos[1])**2
                distance_sqr = x_dist + y_dist
                if distance_sqr < 5**2:
                    self.data[y, x] = TerrainType.GROUND

        # Cave entrance collision
        self.data[end_pos[1]-1:end_pos[1]+2, end_pos[0]:end_pos[0]+2] = TerrainType.WALL
        self.end_sprite_pos = (end_pos[0] - 2, end_pos[1] - 2)
        self.place_end_sprite()

        self.end_position = vector2(
            (end_pos[0] + 0.5) * TILE_SIZE,
            (end_pos[1] + 0.5) * TILE_SIZE,
        )

    def place_start_sprite(self, x, y):
        image = ResourceManager().load_image(Resource.PLANET_START)
        self.place_top_sprite(x, y, image)

    def place_end_sprite(self,):
        image = ResourceManager().load_image(Resource.PLANET_END)
        image = pygame.transform.scale(
            image, [a * 2 for a in image.get_size()]
        )
        self.place_top_sprite(self.end_sprite_pos[0], self.end_sprite_pos[1], image)

    def open_ending(self):
        image = ResourceManager().load_image(Resource.PLANET_END_OPEN)
        image = pygame.transform.scale(
            image, [a * 2 for a in image.get_size()]
        )
        self.place_top_sprite(self.end_sprite_pos[0], self.end_sprite_pos[1], image)
        super().open_ending()