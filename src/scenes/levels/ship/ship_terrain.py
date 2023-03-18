import numpy as np
from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from systems.rng_system import Generator, RngSystem
from systems.resource_manager import Resource, ResourceManager

import pygame


class ShipTerrain(BaseTerrain):
    Y_SIZE = 5
    X_SIZE = 7
    Y_ROOM = 30
    X_ROOM = 22

    def populate(self):
        data = np.full(
            (self.Y_SIZE * self.Y_ROOM, self.X_SIZE * self.X_ROOM),
            TerrainType.NONE,
            dtype=np.int16,
        )

        # Level bounds
        self.data = np.pad(
            data,
            ((self.Y_SIZE * 2, self.Y_SIZE), (self.X_SIZE, self.X_SIZE)),
            mode="constant",
            constant_values=TerrainType.BOUND,
        )
        self.height, self.width = self.data.shape

        # Choose random X for starting room
        rng = RngSystem().get_rng(Generator.MAP)
        self.start_room_x = rng.randint(1, self.X_ROOM)

        base_x = self.start_room_x * self.X_SIZE
        end_x = base_x + self.X_SIZE
        base_y = self.height - self.Y_SIZE * 2
        end_y = base_y + self.Y_SIZE

        # Starting room collision
        self.data[base_y - 2 : end_y + 2, base_x - 3 : end_x + 3] = TerrainType.BOUND
        self.data[base_y - 1 : end_y + 1, base_x - 1 : end_x + 1] = TerrainType.WALL
        self.data[base_y:end_y, base_x:end_x] = TerrainType.GROUND
        self.data[base_y + 2, base_x : base_x + 2] = TerrainType.WALL
        self.data[base_y : base_y + 3, end_x - 1] = TerrainType.WALL
        self.data[base_y - 2, base_x + 2 : base_x + 5] = TerrainType.NONE

        self.starting_tiles = [(base_x + x, base_y - 1) for x in range(2, 5)]
        self.player_starting_position = (
            TILE_SIZE * (base_x + 3.5),
            TILE_SIZE * (base_y + 2.5),
        )

        self.place_start_sprite(base_x - 1, base_y - 2)

    def place_end(self, end_coords):
        room_x = end_coords[0] // self.X_SIZE
        room_y = (end_coords[1] + 1) // self.Y_SIZE - 1

        # Ensure we place this up from a wall
        if end_coords[0] % self.X_SIZE == self.X_SIZE - 1:
            room_x += 1

        base_x = room_x * self.X_SIZE
        end_x = base_x + self.X_SIZE
        base_y = room_y * self.Y_SIZE
        end_y = base_y + self.Y_SIZE

        # Add floor to stand on
        self.data[base_y:end_y, base_x:end_x] = TerrainType.GROUND

        self.end_position = (
            (base_x + 2.5) * TILE_SIZE,
            (base_y + 1.5) * TILE_SIZE,
        )

        self.end_sprite_pos = (base_x, base_y)
        self.place_end_sprite()

    def place_start_sprite(self, x, y):
        image = ResourceManager().load_image(Resource.SHIP_START)
        self.place_top_sprite(x, y, image)

    def place_end_sprite(self):
        image = ResourceManager().load_image(Resource.SHIP_END)
        image = pygame.transform.scale(
            image, [a * 2 for a in image.get_size()]
        )
        self.place_top_sprite(self.end_sprite_pos[0], self.end_sprite_pos[1], image)

    def open_ending(self):
        image = ResourceManager().load_image(Resource.SHIP_END_OPEN)
        image = pygame.transform.scale(
            image, [a * 2 for a in image.get_size()]
        )
        self.place_top_sprite(self.end_sprite_pos[0], self.end_sprite_pos[1], image)
        super().open_ending()
