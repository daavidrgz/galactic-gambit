from noise import snoise2


class BaseGenerator:
    def __init__(
        self,
        generation_mask,
        starting_tile,
        collide_grp,
        pass_grp,
        noise_scale,
        block_scale,
    ):
        self.generation_mask = generation_mask
        self.starting_tile_x, self.starting_tile_y = starting_tile
        self.height, self.width = generation_mask.shape

        self.collide_grp = collide_grp
        self.pass_grp = pass_grp

        self.noise_scale_x, self.noise_scale_y = noise_scale
        self.block_scale_x, self.block_scale_y = block_scale

        import random

        self.coord_offset_x, self.coord_offset_y = (
            (random.random() - 0.5) * 1000000,
            (random.random() - 0.5) * 1000000,
        )  # TODO: Based on seed

    def generate(self):
        pos_queue = [(self.starting_tile_x, self.starting_tile_y)]
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
                self.collide_grp.add(self.get_wall_sprite(curr_pos_x, curr_pos_y))
                continue

            self.pass_grp.add(self.get_ground_sprite(curr_pos_x, curr_pos_y))

            def push(x, y):
                if self.is_pos_available(x, y):
                    pos_queue.append((x, y))
                    self.generation_mask[y, x] = True

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

    def get_wall_sprite(self, x, y):
        raise NotImplementedError

    def get_ground_sprite(self, x, y):
        raise NotImplementedError

    def is_pos_available(self, x, y):
        return (
            x >= 0
            and y >= 0
            and x < self.width
            and y < self.height
            and not self.generation_mask[y, x]
        )
