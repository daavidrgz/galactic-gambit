from enum import Enum, auto
import math
import numpy as np

import pygame

from constants import DESIGN_FRAMERATE


class MagicUpgradeType(Enum):
    INIT = auto()
    UPDATE = auto()


class MagicUpgrade:
    def __init__(self):
        pass

    def apply(self, bullet):
        raise NotImplementedError


class InitMagicUpgrade(MagicUpgrade):
    type = MagicUpgradeType.INIT

    def __init__(self):
        super().__init__()


class DoubleSize(InitMagicUpgrade):
    def __init__(self):
        super().__init__()

    def apply(self, bullet):
        previous_image = bullet.image
        # get pygme surface size
        size = previous_image.get_size()
        # scale the image
        bullet.image = pygame.transform.scale(
            previous_image, (size[0] * 5, size[1] * 5)
        )
        bullet.image_rect = bullet.image.get_rect()
        bullet.rect = bullet.image.get_rect()


class UpdateMagicUpgrade(MagicUpgrade):
    type = MagicUpgradeType.UPDATE

    def __init__(self):
        super().__init__()


class Woobly(UpdateMagicUpgrade):
    def __init__(self):
        super().__init__()
        self.state = 0.0
        self.previous_modify_vector = [0, 0]
        self.frequency = 1 / 300
        self.amplitude = 15

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= 1 / self.frequency
        directionx, directiony = bullet.direction

        modify_vector_module = self.amplitude * math.sin(
            2 * np.pi * self.frequency * self.state
        )

        modify_vector_direction = np.array([directiony, -directionx], dtype=np.float32)
        modify_vector = modify_vector_module * modify_vector_direction
        delta = modify_vector - self.previous_modify_vector
        self.previous_modify_vector = modify_vector
        # TODO: modify direction vector or move it with deltas? It should be the same
        bullet.move(delta)


class ShrinkAndGrow(UpdateMagicUpgrade):
    def __init__(self):
        super().__init__()
        self.state = 0.0
        self.original_image = None
        self.original_rect = None
        self.previous_scale = 0
        self.frequency = 1 / 750
        self.amplitude = 0.75
        self.amplitude_delta = 0.5

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= 1 / self.frequency
        scale = (
            self.amplitude * math.sin(2 * np.pi * self.frequency * self.state)
            + self.amplitude_delta
        )

        if self.original_image is None:
            self.original_image = bullet.image
            self.original_rect = bullet.image_rect

        scale_delta = scale - self.previous_scale
        original_image_size = np.array(self.original_image.get_size())
        scaled_img = pygame.transform.scale(
            self.original_image, (original_image_size * (1 + scale_delta)).astype(int)
        )
        scaled_rect = scaled_img.get_rect()
        previous_position = bullet.rect.center
        bullet.image = scaled_img
        bullet.image_rect = scaled_rect
        bullet.rect = scaled_rect
        bullet.rect.center = previous_position


class SlowAndFast(UpdateMagicUpgrade):
    def __init__(self):
        super().__init__()
        self.state = 0.0
        self.original_speed = None
        self.frequency = 1 / 500
        self.amplitude = 0.75
        self.amplitude_delta = 0.25
        self.phase = np.pi

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= 1 / self.frequency
        scale = (
            self.amplitude
            * np.cbrt(math.sin(2 * np.pi * self.frequency * self.state + self.phase))
            + self.amplitude_delta
        )
        if self.original_speed is None:
            self.original_speed = bullet.speed

        bullet.speed = self.original_speed * (1 + scale)
        bullet.velocity = bullet.speed * bullet.direction
