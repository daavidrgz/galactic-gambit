from noise import snoise2
import pygame
from generation.tile import Tile

from systems.rng_system import Generator, RngSystem


class BaseGenerator:
    def __init__(
        self,
        noise_scale,
        block_scale,
    ):
        self.noise_scale_x, self.noise_scale_y = noise_scale
        self.block_scale_x, self.block_scale_y = block_scale
        self.random_generator = RngSystem.get_instance().get_rng(Generator.MAP)

    def generate(self, terrain):
        # TODO: clear terrain here or in Level class? This way we dont have to remember the call
        # to clear in order to generate a new map. Useful if we do a map level reset like isaac's
        # on level one.
        terrain.clear()
        self.coord_offset_x, self.coord_offset_y = (
            (self.random_generator.random() - 0.5) * 1000000,
            (self.random_generator.random() - 0.5) * 1000000,
        )
        pos_queue = [terrain.starting_tile]
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
                terrain.sprites.add(terrain.get_wall_tile(curr_pos_x, curr_pos_y))
                continue

            terrain.sprites.add(terrain.get_ground_tile(curr_pos_x, curr_pos_y))  # TODO
            terrain.ground_mask[curr_pos_y, curr_pos_x] = True

            def push(x, y):
                if self.is_pos_available(x, y, terrain):
                    pos_queue.append((x, y))
                    terrain.generation_mask[y, x] = True

            push(curr_pos_x + 1, curr_pos_y)
            push(curr_pos_x, curr_pos_y + 1)
            push(curr_pos_x - 1, curr_pos_y)
            push(curr_pos_x, curr_pos_y - 1)

    def noise(self, x, y):
        return snoise2(x, y)

    def noise_wall_condition(self, n, x, y):
        return n > 0.0

    def coordinate_transform(self, x, y):
        return (x, y)

    def is_pos_available(self, x, y, terrain):
        return (
            x >= 0
            and y >= 0
            and x < terrain.width
            and y < terrain.height
            and not terrain.generation_mask[y, x]
        )
