import utils.math

import math
import numpy as np
import pygame

from constants.game_constants import DESIGN_FRAMERATE, TILE_SIZE


class MagicUpgrade:
    init_effect = None
    update_effect = None


class BiggerSize(MagicUpgrade):
    name = "Titan's Might"

    def apply(self, bullet, elapsed_time):
        previous_image = bullet.image
        # get pygme surface size
        previous_size = np.array(previous_image.get_size())
        # scale the image
        bullet.image = pygame.transform.scale(previous_image, previous_size * 1.3)
        bullet.image_rect = bullet.image.get_rect()
        bullet.rect = bullet.image.get_rect()
        bullet.rect.center = bullet.x, bullet.y

    update_effect = apply


# UPDATE UPGRADES
class Woobly(MagicUpgrade):
    name = "Serpent Strike"

    def __init__(self):
        self.state = 0.0
        self.previous_modify_vector = [0, 0]
        self.period = 300
        self.amplitude = 3
        self.phase = np.pi / 2

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= self.period

        modify_vector_module = self.amplitude * math.sin(
            2 * np.pi * self.state / self.period + self.phase
        )

        bullet.velocity = utils.math.rotate_vector(bullet.velocity, modify_vector_module)

    update_effect = apply


class ShrinkAndGrow(MagicUpgrade):
    name = "Waveform Cannon"

    def __init__(self):
        self.state = 0.0
        self.previous_scale = 0
        self.period = 400
        # Scale between 0.8 and 1.4
        self.amplitude = 0.3
        self.amplitude_delta = 1.1

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= self.period
        scale = (
            self.amplitude * math.sin(2 * np.pi * self.state / self.period)
            + self.amplitude_delta
        )

        previous_image = bullet.image
        previous_size = np.array(previous_image.get_size())
        scaled_img = pygame.transform.scale(previous_image, previous_size * scale)
        bullet.image = scaled_img
        bullet.image_rect = scaled_img.get_rect()
        bullet.rect = scaled_img.get_rect()
        bullet.rect.center = bullet.x, bullet.y

    update_effect = apply


class SlowAndFast(MagicUpgrade):
    name = "Crushing Stutter"

    def __init__(self):
        self.state = 0.0
        self.period = 500
        self.amplitude = 0.75
        self.phase = np.pi

    def apply(self, bullet, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.state += elapsed_time
        self.state %= self.period

        velocity_norm = np.linalg.norm(bullet.velocity)

        angle = 2*np.pi * self.state/self.period + self.phase
        divider = 3*self.period * np.cbrt(np.sin(angle))**2
        dT = 2*np.pi * self.amplitude * self.state * np.cos(angle) / (0.1 if abs(divider) < 0.1 else divider)

        new_speed = np.clip(velocity_norm + dT * elapsed_units, 3, 50)

        bullet.velocity = (bullet.velocity / velocity_norm) * new_speed

    def setup(self, bullet, level):
        bullet.velocity *= 0.75

    update_effect = apply
    init_effect = setup


class Rainbow(MagicUpgrade):
    name = "Prismatic Aura"

    def __init__(self):
        self.state = 0.0
        self.laps = 2

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= 360 * self.laps

    def setup(self, bullet, level):
        bullet.add_image_modifier(self.__rainbow_modifier)

    def __rainbow_modifier(self, image):
        color = pygame.Color(0)
        color.hsva = ((self.state / self.laps) % 360, 50, 100, 100)
        hit_mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        hit_mask.fill(color)
        image.blit(hit_mask, (0, 0), special_flags=pygame.BLEND_MULT)

    update_effect = apply
    init_effect = setup

class Gravity(MagicUpgrade):
    name = "Portable Instability"

    def apply(self, bullet, elapsed_time):
        if self.timer < 50:
            self.timer += elapsed_time
            return

        bullet_x, bullet_y = bullet.get_position()
        player_x, player_y = self.player.get_position()

        direction = np.array((player_x - bullet_x, player_y - bullet_y))
        distance = np.linalg.norm(direction)
        direction /= distance

        distance = np.clip(distance / TILE_SIZE / 2.0, 1, 20)

        bullet.velocity += (direction * elapsed_time * 0.1) / distance**2

    def setup(self, bullet, level):
        self.timer = 0
        self.player = level.get_player()

    update_effect = apply
    init_effect = setup

class Ghost(MagicUpgrade):
    name = "Ghostly Shot"

    def setup(self, bullet, level):
        bullet.ground_collision = False
        bullet.add_image_modifier(self.__translucent_modifier)

    def __translucent_modifier(self, image):
        image.set_alpha(127)

    init_effect = setup
