from systems.resource_manager import Resource
from utils.math import rotate_vector, square_norm, rotate_vector_rad, tvector2

import math
import numpy as np
import pygame
import heapq

from constants.game_constants import DESIGN_FRAMERATE, TILE_SIZE


class MagicUpgrade:
    init_effect = None
    update_effect = None


class TitansMight(MagicUpgrade):
    name = "Titan's Might"
    icon = Resource.BIGGER_SIZE_ICON
    order = 0

    def apply(self, bullet, elapsed_time):
        previous_image = bullet.image
        # Get pygme surface size
        previous_size = tvector2(previous_image.get_size())
        # Scale the image
        bullet.set_image(pygame.transform.scale(previous_image, previous_size * 1.7))
        # Increase logical size
        bullet.size *= 1.7
        # Make it knock things harder
        bullet.knockback *= 3

    init_effect = apply


# UPDATE UPGRADES
class SerpentStrike(MagicUpgrade):
    name = "Serpent Strike"
    icon = Resource.SNAKE_ICON
    order = 5

    def __init__(self):
        self.state = 0.0
        self.period = 300
        self.amplitude = 3
        self.phase = np.pi / 2

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= self.period

        modify_vector_module = self.amplitude * math.sin(
            2 * np.pi * self.state / self.period + self.phase
        )

        bullet.velocity = rotate_vector(bullet.velocity, modify_vector_module)

    def setup(self, bullet, level):
        bullet.knockback *= 1.2
        bullet.damage += 1.0

    update_effect = apply
    init_effect = setup


class WaveformCannon(MagicUpgrade):
    name = "Waveform Cannon"
    icon = Resource.WAVEFORM_ICON
    order = 6

    def __init__(self):
        self.state = 0.0
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

        # Scale sprite
        previous_image = bullet.image
        size = tvector2(previous_image.get_size()) * scale
        bullet.set_temp_image(pygame.transform.scale(previous_image, size))

        # Scale logical size
        bullet.size = self.initial_size * scale

        # Wobble stats
        bullet.damage = self.initial_damage * scale
        bullet.knockback = self.initial_knockback * scale

    def setup(self, bullet, level):
        self.initial_size = bullet.size
        self.initial_damage = bullet.damage
        self.initial_knockback = bullet.knockback

    update_effect = apply
    init_effect = setup


class CrushingStutter(MagicUpgrade):
    name = "Crushing Stutter"
    icon = Resource.SLOW_AND_FAST_ICON
    order = 4

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

        angle = 2 * np.pi * self.state / self.period + self.phase
        divider = 3 * self.period * np.cbrt(np.sin(angle)) ** 2
        dT = (
            2
            * np.pi
            * self.amplitude
            * self.state
            * np.cos(angle)
            / (0.1 if abs(divider) < 0.1 else divider)
        )

        new_speed = np.clip(velocity_norm + dT * elapsed_units, 3, 50)

        bullet.velocity = (bullet.velocity / velocity_norm) * new_speed

    def setup(self, bullet, level):
        bullet.velocity *= 0.75

    update_effect = apply
    init_effect = setup


class PrismaticAura(MagicUpgrade):
    name = "Prismatic Aura"
    icon = Resource.PRISM_ICON
    order = 7

    def __init__(self):
        self.state = 0.0
        self.laps = 2

    def apply(self, bullet, elapsed_time):
        self.state += elapsed_time
        self.state %= 360 * self.laps

    def setup(self, bullet, level):
        bullet.add_image_modifier(self.__rainbow_modifier)

        # +20% damage
        bullet.damage *= 1.2

    def __rainbow_modifier(self, image):
        color = pygame.Color(0)
        color.hsva = ((self.state / self.laps) % 360, 50, 100, 100)
        hit_mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        hit_mask.fill(color)
        image.blit(hit_mask, (0, 0), special_flags=pygame.BLEND_MULT)

    update_effect = apply
    init_effect = setup


class PortableInstability(MagicUpgrade):
    name = "Portable Instability"
    icon = Resource.BLACKHOLE_ICON
    order = 2

    def apply(self, bullet, elapsed_time):
        if self.timer < 170:
            self.timer += elapsed_time
            return

        direction = self.player.position - bullet.position
        distance = np.linalg.norm(direction)
        direction /= distance

        distance = np.clip(distance / TILE_SIZE / 2.0, 1, 20)

        # Pull towards player
        bullet.velocity += (direction * elapsed_time * 0.14) / distance**1.5

    def setup(self, bullet, level):
        self.timer = 0
        self.player = level.get_player()
        bullet.lifetime *= 5

    update_effect = apply
    init_effect = setup


class GhostlyShot(MagicUpgrade):
    name = "Ghostly Shot"
    icon = Resource.GHOST_ALT_ICON
    order = 1

    def setup(self, bullet, level):
        # No collision
        bullet.ground_collision = False

        # Translucent
        bullet.add_image_modifier(self.__translucent_modifier)

        # Reduced range
        bullet.lifetime *= 0.8

    def __translucent_modifier(self, image):
        image.set_alpha(127)

    init_effect = setup


class ViciousAim(MagicUpgrade):
    name = "Vicious Aim"
    icon = Resource.AIM_ICON
    order = 3

    def __choose_target(self, bullet):
        target = None

        from_pos = bullet.position

        to_remove = []
        min_distance = np.inf
        for i, enemy in enumerate(self.targets):
            if enemy.removed:
                to_remove.append(i)
                continue

            distance = square_norm(enemy.position - from_pos)
            if distance < min_distance:
                min_distance = distance
                target = enemy

        for i in reversed(to_remove):
            self.targets.pop(i)

        return target, min_distance

    def apply(self, bullet, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000
        target, sqr_dist = self.__choose_target(bullet)

        if not target:
            return

        angle = np.arctan2(bullet.velocity[1], bullet.velocity[0])
        diff_vector = rotate_vector_rad(target.position - bullet.position, -angle)
        angle = np.arctan2(diff_vector[1], diff_vector[0])

        if angle > np.pi:
            angle -= 2 * np.pi

        angle /= sqr_dist / TILE_SIZE / 10

        if abs(angle) > 0.15 * elapsed_units:
            angle = np.sign(angle) * 0.15 * elapsed_units

        # Home in on enemies
        bullet.velocity = rotate_vector_rad(bullet.velocity, angle)

    def setup(self, bullet, level):
        bullet.velocity *= 0.7
        bullet.lifetime /= 0.7

        from_pos = bullet.position
        self.target = None

        def enemy_distance(enemy):
            return square_norm(enemy.position - from_pos)

        self.targets = heapq.nsmallest(5, level.enemy_group, enemy_distance)

    update_effect = apply
    init_effect = setup
