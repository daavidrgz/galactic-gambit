from enum import Enum, auto
import math
import numpy as np

import pygame


class MagicUpgradeType(Enum):
    INIT = auto()
    UPDATE = auto()


class MagicUpgrade:
    def __init__(self):
        pass

    def apply(self, bullet):
        raise NotImplementedError

    def setup(self, bullet):
        pass


class InitMagicUpgrade(MagicUpgrade):
    # This class applies an upgrade to a bullet when it is created
    type = MagicUpgradeType.INIT

    def __init__(self):
        super().__init__()


class UpdateMagicUpgrade(MagicUpgrade):
    # This class applies an upgrade to a bullet every frame
    type = MagicUpgradeType.UPDATE

    def __init__(self):
        super().__init__()
        self.type = MagicUpgradeType.UPDATE


# # INIT UPGRADES
# FIXME: Broken
# class BiggerSize(InitMagicUpgrade):
#     name = "Bigger Size"

#     def __init__(self):
#         super().__init__()

#     def apply(self, bullet):
#         previous_image = bullet.image
#         # get pygme surface size
#         size = previous_image.get_size()
#         # scale the image
#         bullet.image = pygame.transform.scale(
#             previous_image, (size[0] * 1.3, size[1] * 1.3)
#         )
#         bullet.image_rect = bullet.image.get_rect()
#         bullet.rect = bullet.image.get_rect()


# UPDATE UPGRADES
class Woobly(UpdateMagicUpgrade):
    name = "Woobly"

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


# FIXME: Broken
# class ShrinkAndGrow(UpdateMagicUpgrade):
#     name = "Shrink and Grow"

#     def __init__(self):
#         super().__init__()
#         self.state = 0.0
#         self.original_image = None
#         self.original_rect = None
#         self.previous_scale = 0
#         self.frequency = 1 / 750
#         self.amplitude = 0.3
#         self.amplitude_delta = 1.2

#     def apply(self, bullet, elapsed_time):
#         if self.original_image is None:
#             self.original_rect = bullet.image_rect

#         self.state += elapsed_time
#         self.state %= 1 / self.frequency
#         scale = (
#             self.amplitude * math.sin(2 * np.pi * self.frequency * self.state)
#             + self.amplitude_delta
#         )

#         scale_delta = scale - self.previous_scale
#         original_image_size = np.array(self.original_image.get_size())
#         scaled_img = pygame.transform.scale(
#             self.original_image, (original_image_size * scale_delta).astype(int)
#         )
#         scaled_rect = scaled_img.get_rect()
#         previous_position = bullet.rect.center
#         bullet.image = scaled_img
#         bullet.image_rect = scaled_rect
#         bullet.rect = scaled_rect
#         bullet.rect.center = previous_position


class SlowAndFast(UpdateMagicUpgrade):
    name = "Slow and Fast"

    def __init__(self):
        super().__init__()
        self.state = 0.0
        self.original_speed = None
        self.frequency = 1 / 500
        self.amplitude = 0.75
        self.amplitude_delta = 0.25
        self.phase = np.pi

    def apply(self, bullet, elapsed_time):
        if self.original_speed is None:
            self.original_speed = bullet.speed
        self.state += elapsed_time
        self.state %= 1 / self.frequency
        scale = (
            self.amplitude
            * np.cbrt(math.sin(2 * np.pi * self.frequency * self.state + self.phase))
            + self.amplitude_delta
        )

        bullet.speed = self.original_speed * (1 + scale)
        bullet.velocity = bullet.speed * bullet.direction


class Rainbow(UpdateMagicUpgrade):
    name = "Rainbow"

    def __init__(self):
        super().__init__()
        self.state = 0.0
        self.laps = 2

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= 360 * self.laps

    def setup(self, bullet):
        bullet.add_image_modifier(self.__rainbow_modifier)

    def __rainbow_modifier(self, image):
        color = pygame.Color(0)
        color.hsva = ((self.state / self.laps) % 360, 50, 100, 100)
        hit_mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        hit_mask.fill(color)
        image.blit(hit_mask, (0, 0), special_flags=pygame.BLEND_MULT)
