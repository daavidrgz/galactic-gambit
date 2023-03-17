import numpy as np
from entities.living.enemies.ranged_enemies.base_ranged_enemy import BaseRangedEnemy
from ai.ranged_ai import RangedAI
from systems.resource_manager import Resource


class RangedEnemy3(BaseRangedEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 2
        self.ai = RangedAI(500, 600, 400, 200)
        self.drag = 0.25
        self.speed = 0.7

        self.damage = 4
        self.knockback = 10
        self.projectile_speed = 8
        self.attack_lifetime = 800
        self.reload_speed = 1000

        self.walk_right = Resource.RANGED3_WALK_RIGHT
        self.walk_left = Resource.RANGED3_WALK_LEFT
        self.idle_right = Resource.RANGED3_IDLE_RIGHT
        self.idle_left = Resource.RANGED3_IDLE_LEFT
        self.hurt_right = Resource.RANGED3_HURT_RIGHT
        self.hurt_left = Resource.RANGED3_HURT_LEFT
        self.dead_right = Resource.RANGED3_DEAD_RIGHT
        self.dead_left = Resource.RANGED3_DEAD_LEFT

        self.attack_image = Resource.LASER

        super().__init__(
            self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed
        )

    def trigger_attack(self):
        super().trigger_attack(
            self.attack_image,
            self.damage,
            self.knockback,
            self.projectile_speed,
            self.attack_lifetime,
            self.reload_speed,
        )

    def update(self, elapsed_time):
        super().update(
            elapsed_time,
            self.walk_right,
            self.walk_left,
            self.idle_right,
            self.idle_left,
        )

    def hit(self, damage, knockback=None):
        super().hit(damage, self.hurt_right, self.hurt_left, knockback)

    def on_death(self):
        super().on_death(self.dead_right, self.dead_left)