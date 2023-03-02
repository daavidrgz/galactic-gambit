from noise import snoise2
from generation.tile import Tile

from systems.rng_system import Generator, RngSystem


class BaseGenerator:
    def __init__(
        self,
        noise_scale,
        block_scale,
        terrain
    ):
        self.noise_scale_x, self.noise_scale_y = noise_scale
        self.block_scale_x, self.block_scale_y = block_scale
        self.terrain = terrain
        self.random_generator = RngSystem.get_instance().get_rng(Generator.MAP)

    def generate(self):
        self.coord_offset_x, self.coord_offset_y = (
            (self.random_generator.random() - 0.5) * 1000000,
            (self.random_generator.random() - 0.5) * 1000000,
        )
        pos_queue = [self.terrain.starting_tile]
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
                self.terrain.sprites.add(self.get_wall_tile(curr_pos_x, curr_pos_y))
                continue

            self.terrain.sprites.add(self.get_ground_tile(curr_pos_x, curr_pos_y))  # TODO
            self.terrain.ground_mask[curr_pos_y, curr_pos_x] = True

            def push(x, y):
                if self.is_pos_available(x, y):
                    pos_queue.append((x, y))
                    self.terrain.generation_mask[y, x] = True

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

    def is_pos_available(self, x, y):
        return (
            x >= 0
            and y >= 0
            and x < self.terrain.width
            and y < self.terrain.height
            and not self.terrain.generation_mask[y, x]
        )
    
    # Template pattern
    def get_wall_tile(self, x, y):
        return Tile(x, y, self.get_wall_sprite(x, y))

    def get_ground_tile(self, x, y):
        return Tile(x, y, self.get_ground_sprite(x, y))

    def get_wall_sprite(self, x, y):
        raise NotImplementedError

    def get_ground_sprite(self, x, y):
        raise NotImplementedError
