from utils.singleton import Singleton

import numpy as np
from noise import pnoise1

from constants.game_constants import (
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    DESIGN_FRAMERATE,
    CAMERA_LAG_BEHIND,
    CAMERA_SHAKE_SPEED,
    CAMERA_SHAKE_AMOUNT,
)


class CameraManager(metaclass=Singleton):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.shake = 0.0

    def update(self, elapsed_time):
        direction = np.array(
            [self.target_x - self.x, self.target_y - self.y], dtype=np.float64
        )
        direction *= elapsed_time * DESIGN_FRAMERATE / 1000.0 / CAMERA_LAG_BEHIND

        if np.linalg.norm(direction) < 0.2:
            direction = np.zeros(2)

        self.x = self.x + direction[0]
        self.y = self.y + direction[1]

        if self.shake > 0.0:
            self.x += (
                pnoise1(self.shake * CAMERA_SHAKE_SPEED)
                * self.shake
                * CAMERA_SHAKE_AMOUNT
            )
            self.y += (
                pnoise1(self.shake * CAMERA_SHAKE_SPEED + 2711.0)
                * self.shake
                * CAMERA_SHAKE_AMOUNT
            )

            self.shake -= elapsed_time / 1000.0

    def set_coords(self, coords):
        self.x, self.y = coords

    def get_coords(self):
        return self.x, self.y

    def set_center(self, coords):
        self.x = coords[0] - DESIGN_WIDTH // 2
        self.y = coords[1] - DESIGN_HEIGHT // 2

    def get_center(self):
        return (self.x + DESIGN_WIDTH // 2, self.y + DESIGN_HEIGHT // 2)

    def set_target_center(self, coords):
        self.target_x = coords[0] - DESIGN_WIDTH // 2
        self.target_y = coords[1] - DESIGN_HEIGHT // 2

    def set_shake(self, shake):
        self.shake = shake
