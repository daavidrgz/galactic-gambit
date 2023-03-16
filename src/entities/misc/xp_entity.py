from entities.entity import Entity
from systems.rng_system import RngSystem, Generator
from systems.resource_manager import Resource
import utils.math

import numpy as np
from noise import pnoise1

from constants.game_constants import TILE_SIZE

class XpEntity(Entity):
    def __init__(self, initial_pos, amount):
        super().__init__(Resource.XP, initial_pos)

        self.amount = amount
        self.velocity = np.zeros(2)
        self.timer = 0

    def setup(self, level):
        super().setup(level)
        rng = RngSystem().get_rng(Generator.ENEMIES)
        self.noise_seed = rng.randint(0, 10000)

        self.player = level.get_player()
        player_x, player_y = self.player.get_position()
        direction = np.array((player_x - self.x, player_y - self.y))
        distance = np.linalg.norm(direction)
        direction /= distance * 3
        self.velocity = utils.math.rotate_vector(direction, 90.0 + 180.0 * rng.random())

    def update(self, elapsed_time):
        player_x, player_y = self.player.get_position()
        direction = np.array((player_x - self.x, player_y - self.y))
        distance = np.linalg.norm(direction)
        direction /= distance

        distance = min(distance / TILE_SIZE, 15)
        if distance < 2:
            self.player.increase_exp(self.amount)
            self.kill()
            return
        
        self.timer += elapsed_time
        noise_factor = distance**2 / 15**2 * 0.1 * elapsed_time
        self.move((
            pnoise1(self.timer / 1000.0 + self.noise_seed) * noise_factor,
            pnoise1(self.timer / 1000.0 + self.noise_seed + 20711.0) * noise_factor,
        ))

        self.velocity += (direction * 0.1) / distance**2 * elapsed_time
        self.velocity *= 1.0 - (0.001 * elapsed_time)

        self.move(self.velocity * elapsed_time)

        super().update(elapsed_time)
