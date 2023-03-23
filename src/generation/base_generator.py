from generation.tile import Tile
from generation.base_terrain import TerrainType
from systems.rng_system import Generator, RngSystem

from noise import snoise2
import numpy as np


class BaseGenerator:
    def __init__(self, noise_scale, block_scale, terrain, desired_area):
        self.noise_scale_x, self.noise_scale_y = noise_scale
        self.block_scale_x, self.block_scale_y = block_scale
        self.terrain = terrain

        # Use the map rng, to ensure seed consistency
        self.rng = RngSystem.get_instance().get_rng(Generator.MAP)

        self.explored_tiles = 0
        self.min_tiles, self.max_tiles = desired_area

    def generate(self):
        # Ensure levels are not too small, rerunning the fastest steps of the algorithm
        while (
            self.explored_tiles < self.min_tiles or self.explored_tiles > self.max_tiles
        ):
            # Place the starting room and terrain bounds
            self.terrain.clear()
            self.terrain.populate()

            # Search the grid from the starting room
            self.explore_graph()

        # After we know the rest of the level layout, place the final room
        self.terrain.place_end(self.end)

        # Choose what sprites to display for each tile
        self.place_sprites()

        # Render the level to a buffer, so it can be then blitted just once per frame
        self.terrain.generate_buffer()

    def explore_graph(self):
        # We offset the noise based on the seeded rng
        self.coord_offset_x, self.coord_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

        start_x, start_y = self.terrain.player_starting_position
        max_distance = 0

        # Start search at coords gived by the terrain
        pos_queue = [(x, y, 0) for x, y in self.terrain.starting_tiles]
        self.explored_tiles = 0
        while len(pos_queue) > 0:
            curr_pos_x, curr_pos_y, depth = pos_queue.pop(0)
            self.explored_tiles += 1

            # Compute the custom distance function for this tile
            distance = self.distance_function(
                start_x, start_y, curr_pos_x, curr_pos_y, depth
            )
            # If it's the furthest we've gone, store it as the end position
            if distance > max_distance:
                max_distance = distance
                self.end = (curr_pos_x, curr_pos_y)

            # Transform coordinates to shape noise
            working_pos_x = curr_pos_x - curr_pos_x % self.block_scale_x
            working_pos_y = curr_pos_y - curr_pos_y % self.block_scale_y
            working_pos_x, working_pos_y = self.coordinate_transform(
                working_pos_x, working_pos_y
            )

            # Compute noise function
            n = self.noise(
                working_pos_x / self.noise_scale_x - self.coord_offset_x,
                working_pos_y / self.noise_scale_y - self.coord_offset_x,
            )

            # Check if a wall should go on this tile
            if self.noise_wall_condition(n, working_pos_x, working_pos_y):
                self.terrain.data[curr_pos_y, curr_pos_x] = TerrainType.WALL
                continue # Don't visit wall neighbors

            self.terrain.data[curr_pos_y, curr_pos_x] = TerrainType.GROUND

            # Visit neighbors with 4-adjacency
            self.push(pos_queue, curr_pos_x + 1, curr_pos_y, depth)
            self.push(pos_queue, curr_pos_x, curr_pos_y + 1, depth)
            self.push(pos_queue, curr_pos_x - 1, curr_pos_y, depth)
            self.push(pos_queue, curr_pos_x, curr_pos_y - 1, depth)

    # Pushes a neighbor to the queue, only if it's available to generate
    def push(self, pos_queue, x, y, depth):
        if self.terrain.in_bounds(x, y):
            if self.terrain.data[y, x] == TerrainType.NONE:
                pos_queue.append((x, y, depth + 1))
                self.terrain.data[y, x] = TerrainType.GENERATING
            elif self.terrain.data[y, x] == TerrainType.BOUND:
                self.terrain.data[y, x] = TerrainType.WALL

    # Slides a 3x3 tile window across the grid, using it to decide which sprites to show
    def place_sprites(self):
        stride = np.lib.stride_tricks.sliding_window_view(self.terrain.data, (3, 3))
        for y, y_view in enumerate(stride):
            for x, w in enumerate(y_view):
                tile = self.get_tile(x + 1, y + 1, w)
                if tile is None:
                    continue

                self.terrain.sprites.add(tile)

    # Noise function may be replaced by subclasses
    def noise(self, x, y):
        return snoise2(x, y)

    # Wall condition may be replaced by subclasses
    def noise_wall_condition(self, n, x, y):
        return n > 0.0

    # Coordinate transformation may be replaced by subclasses
    def coordinate_transform(self, x, y):
        return (x, y)

    # Distance function may use both coords and search depth
    def distance_function(self, x0, y0, x1, y1, depth):
        return abs(x0 - x1) + abs(y0 - y1)

    # Template pattern
    def get_tile(self, x, y, surroundings):
        sprite = self.get_sprite(x, y, surroundings)
        if sprite is None:
            return None

        return Tile(x, y, self.get_sprite(x, y, surroundings))

    def get_sprite(self, x, y, surroundings):
        raise NotImplementedError
