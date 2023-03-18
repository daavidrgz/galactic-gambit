import numpy as np
from entities.living.enemies.melee_enemies.base_melee_enemy import BaseMeleeEnemy
from ai.melee_ai import MeleeAI
from systems.resource_manager import Resource, ResourceManager


class MeleeEnemy1(BaseMeleeEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 4
        self.ai = MeleeAI(400, 500, 100)
        self.drag = 0.25
        self.speed = 1.5

        self.damage = 2
        self.knockback = 10
        self.projectile_speed = 5
        self.attack_lifetime = 100

        self.walk_right = Resource.MELEE1_WALK_RIGHT
        self.walk_left = Resource.MELEE1_WALK_LEFT
        self.idle_right = Resource.MELEE1_IDLE_RIGHT
        self.idle_left = Resource.MELEE1_IDLE_LEFT
        self.hurt_right = Resource.MELEE1_HURT_RIGHT
        self.hurt_left = Resource.MELEE1_HURT_LEFT
        self.dead_right = Resource.MELEE1_DEAD_RIGHT
        self.dead_left = Resource.MELEE1_DEAD_LEFT

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
