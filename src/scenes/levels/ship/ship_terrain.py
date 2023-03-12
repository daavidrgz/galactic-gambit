import numpy as np
from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from systems.rng_system import Generator, RngSystem


class ShipTerrain(BaseTerrain):
    def populate(self):
        Y_ROOM_SIZE = 5
        X_ROOM_SIZE = 7
        Y_ROOMS = 30
        X_ROOMS = 22
        data = np.full(
            (Y_ROOM_SIZE * Y_ROOMS, X_ROOM_SIZE * X_ROOMS),
            TerrainType.NONE,
            dtype=np.int16,
        )
        self.data = np.pad(
            data,
            ((Y_ROOM_SIZE * 2, Y_ROOM_SIZE), (X_ROOM_SIZE, X_ROOM_SIZE)),
            mode="constant",
            constant_values=TerrainType.BOUND,
        )
        self.height, self.width = self.data.shape

        rng = RngSystem().get_rng(Generator.MAP)
        self.start_room_x = rng.randint(1, X_ROOMS)

        base_x = self.start_room_x * X_ROOM_SIZE
        end_x = base_x + X_ROOM_SIZE
        base_y = self.height - Y_ROOM_SIZE * 2
        end_y = base_y + Y_ROOM_SIZE

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
