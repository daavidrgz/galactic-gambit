import math

import numpy as np
from constants.game_constants import SPEED_EPSILON
from entities.projectile.player_bullet import PlayerBullet


class Gun:
    def __init__(
        self, damage, cooldown, bullet_speed, gun_offset, spread, n_bullets, knockback
    ):
        self.damage = damage
        self.cooldown = cooldown
        self.current_cooldown = 0.0
        self.bullet_speed = bullet_speed
        self.gun_offset = gun_offset
        self.spread = spread
        self.n_bullets = n_bullets
        self.knockback = knockback

        self.upgrades = []

    def add_magical_upgrade(self, upgrade):
        self.upgrades.append(upgrade)

    def is_ready(self):
        return self.current_cooldown == 0.0

    def update_cooldown(self, elapsed_time):
        self.current_cooldown = max(0.0, self.current_cooldown - elapsed_time)

    def shoot(self, shoot_position, facing_vector):
        self.current_cooldown = self.cooldown
        return self.generate_bullets(shoot_position, facing_vector)

    def __instantiate_upgrades(self):
        return [upgrade() for upgrade in self.upgrades]

    def generate_bullets(self, shoot_position, facing_vector):
        # TODO: If spread angle is negative, it should have negative spread?
        # or just take max(0,spread)?
        bullets = []
        half_spread = self.spread / 2

        spread_step = self.spread / self.n_bullets
        facingy, facingx = facing_vector
        facing_vector_angle = math.atan2(-facingy, facingx)
        initial_angle = facing_vector_angle - half_spread
        for i in range(0, self.n_bullets):
            # rotate facing vector i*15 degrees
            vector_angle = initial_angle + i * spread_step
            new_facingy = -math.sin(vector_angle)
            new_facingx = math.cos(vector_angle)
            new_facing_vector = np.array([new_facingy, new_facingx])
            initial_position = shoot_position + new_facing_vector * self.gun_offset
            upgrades_instance = self.__instantiate_upgrades()
            new_bullet = PlayerBullet(
                initial_position,
                self.bullet_speed,
                new_facing_vector,
                self.damage,
                self.knockback,
                upgrades_instance,
            )
            bullets.append(new_bullet)
        return bullets
