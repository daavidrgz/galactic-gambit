import numpy as np
from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from systems.rng_system import Generator, RngSystem


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
        self.data = np.pad(
            data,
            ((self.Y_SIZE * 2, self.Y_SIZE), (self.X_SIZE, self.X_SIZE)),
            mode="constant",
            constant_values=TerrainType.BOUND,
        )
        self.height, self.width = self.data.shape

        rng = RngSystem().get_rng(Generator.MAP)
        self.start_room_x = rng.randint(1, self.X_ROOM)

        base_x = self.start_room_x * self.X_SIZE
        end_x = base_x + self.X_SIZE
        base_y = self.height - self.Y_SIZE * 2
        end_y = base_y + self.Y_SIZE

        for x in range(base_x - 3, end_x + 3):
            for y in range(base_y - 2, end_y + 2):
                self.data[y, x] = TerrainType.BOUND

        for x in range(base_x - 1, end_x + 1):
            for y in range(base_y - 1, end_y + 1):
                self.data[y, x] = TerrainType.WALL

        for x in range(base_x, end_x):
            for y in range(base_y, end_y):
                self.data[y, x] = TerrainType.GROUND

        for x in range(base_x + 2, base_x + 5):
            self.data[base_y - 2, x] = TerrainType.NONE

        self.player_starting_position = (
            TILE_SIZE * (base_x + 3.5),
            TILE_SIZE * (base_y + 2.5),
        )

        self.starting_tiles = [(base_x + x, base_y - 1) for x in range(2, 5)]

    def place_end(self, end_coords):
        room_x = end_coords[0] // self.X_SIZE
        room_y = (end_coords[1] + 1) // self.Y_SIZE - 1

        base_x = room_x * self.X_SIZE
        end_x = base_x + self.X_SIZE
        base_y = room_y * self.Y_SIZE
        end_y = base_y + self.Y_SIZE

        for x in range(base_x, end_x):
            for y in range(base_y, end_y):
                self.data[y, x] = TerrainType.GROUND

        for x in range(base_x + 2, end_x - 2):
            for y in range(base_y + 1, end_y - 1):
                self.data[y, x] = TerrainType.WALL
