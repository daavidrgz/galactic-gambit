from generation.tile import Tile
from generation.base_terrain import TerrainType
from systems.rng_system import Generator, RngSystem

from noise import snoise2
import numpy as np


class BaseGenerator:
    def __init__(self, noise_scale, block_scale, terrain):
        self.noise_scale_x, self.noise_scale_y = noise_scale
        self.block_scale_x, self.block_scale_y = block_scale
        self.terrain = terrain
        self.rng = RngSystem.get_instance().get_rng(Generator.MAP)

    def generate(self):
        self.terrain.clear()
        self.terrain.populate()
        self.explore_graph()
        # TODO: Fix imperfections
        # TODO: Place level end
        self.place_sprites()
        self.terrain.generate_buffer()

    def explore_graph(self):
        self.coord_offset_x, self.coord_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

        pos_queue = list(self.terrain.starting_tiles)
        while len(pos_queue) > 0:
            curr_pos_x, curr_pos_y = pos_queue.pop()

            working_pos_x = curr_pos_x - curr_pos_x % self.block_scale_x
            working_pos_y = curr_pos_y - curr_pos_y % self.block_scale_y
            working_pos_x, working_pos_y = self.coordinate_transform(
                working_pos_x, working_pos_y
            )

            n = self.noise(
                working_pos_x / self.noise_scale_x - self.coord_offset_x,
                working_pos_y / self.noise_scale_y - self.coord_offset_x,
            )

            if self.noise_wall_condition(n, working_pos_x, working_pos_y):
                self.terrain.data[curr_pos_y, curr_pos_x] = TerrainType.WALL
                continue

            self.terrain.data[curr_pos_y, curr_pos_x] = TerrainType.GROUND

            def push(x, y):
                if self.terrain.in_bounds(x, y):
                    if self.terrain.data[y, x] == TerrainType.NONE:
                        pos_queue.append((x, y))
                        self.terrain.data[y, x] = TerrainType.GENERATING
                    elif self.terrain.data[y, x] == TerrainType.BOUND:
                        self.terrain.data[y, x] = TerrainType.WALL

            push(curr_pos_x + 1, curr_pos_y)
            push(curr_pos_x, curr_pos_y + 1)
            push(curr_pos_x - 1, curr_pos_y)
            push(curr_pos_x, curr_pos_y - 1)

    def place_sprites(self):
        stride = np.lib.stride_tricks.sliding_window_view(self.terrain.data, (3, 3))
        for y, y_view in enumerate(stride):
            for x, w in enumerate(y_view):
                tile = self.get_tile(x + 1, y + 1, w)
                if tile is None:
                    continue

                self.terrain.sprites.add(tile)

    def noise(self, x, y):
        return snoise2(x, y)

    def noise_wall_condition(self, n, x, y):
        return n > 0.0

    def coordinate_transform(self, x, y):
        return (x, y)

    # Template pattern
    def get_tile(self, x, y, surroundings):
        sprite = self.get_sprite(x, y, surroundings)
        if sprite is None:
            return None

        return Tile(x, y, self.get_sprite(x, y, surroundings))

    def get_sprite(self, x, y, surroundings):
        raise NotImplementedError
