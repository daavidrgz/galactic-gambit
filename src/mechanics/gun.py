import math

import numpy as np
from constants.game_constants import SPEED_EPSILON
from entities.projectile.player_bullet import PlayerBullet
from mechanics.magic.magic_upgrade import MagicUpgradeType


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

        self.init_upgrades = []
        self.update_upgrades = []

    def add_magical_upgrade(self, upgrade):
        if upgrade.type == MagicUpgradeType.INIT:
            self.init_upgrades.append(upgrade)
        elif upgrade.type == MagicUpgradeType.UPDATE:
            self.update_upgrades.append(upgrade)
        else:
            raise ValueError("Upgrade type not recognized")

    def is_ready(self):
        return self.current_cooldown == 0.0

    def update_cooldown(self, elapsed_time):
        self.current_cooldown = max(0.0, self.current_cooldown - elapsed_time)

    def shoot(self, shoot_position, facing_vector):
        self.current_cooldown = self.cooldown
        return self.generate_bullets(shoot_position, facing_vector)

    def __init_upgrades(self, upgrades):
        return [upgrade() for upgrade in upgrades]

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
            # Use epsilon to avoid floating point errors with cosine and sine
            if new_facingy < SPEED_EPSILON and new_facingy > -SPEED_EPSILON:
                new_facingy = 0
            if new_facingx < SPEED_EPSILON and new_facingx > -SPEED_EPSILON:
                new_facingx = 0

            new_facing_vector = np.array([new_facingy, new_facingx])
            initial_position = shoot_position + new_facing_vector * self.gun_offset
            init_upgrades = self.__init_upgrades(self.init_upgrades)
            update_upgrades = self.__init_upgrades(self.update_upgrades)
            new_bullet = PlayerBullet(
                initial_position,
                self.bullet_speed,
                new_facing_vector,
                self.damage,
                self.knockback,
                init_upgrades,
                update_upgrades,
            )
            # Setup upgrades
            [upgrade.setup(new_bullet) for upgrade in init_upgrades]
            [upgrade.setup(new_bullet) for upgrade in update_upgrades]
            bullets.append(new_bullet)
        return bullets
