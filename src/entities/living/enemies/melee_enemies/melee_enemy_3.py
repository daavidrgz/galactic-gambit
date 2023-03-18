import numpy as np
from entities.living.enemies.melee_enemies.base_melee_enemy import BaseMeleeEnemy
from ai.melee_ai import MeleeAI
from systems.resource_manager import Resource, ResourceManager


class MeleeEnemy3(BaseMeleeEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 2
        self.ai = MeleeAI(500, 600, 50)
        self.drag = 0.25
        self.speed = 2.5

        self.damage = 1
        self.knockback = 10
        self.projectile_speed = 5
        self.attack_lifetime = 100
        self.reload_speed = 30

        self.walk_right = Resource.MELEE3_WALK_RIGHT
        self.walk_left = Resource.MELEE3_WALK_LEFT
        self.idle_right = Resource.MELEE3_IDLE_RIGHT
        self.idle_left = Resource.MELEE3_IDLE_LEFT
        self.hurt_right = Resource.MELEE3_HURT_RIGHT
        self.hurt_left = Resource.MELEE3_HURT_LEFT
        self.dead_right = Resource.MELEE3_DEAD_RIGHT
        self.dead_left = Resource.MELEE3_DEAD_LEFT

        self.attack_image = Resource.LASER

        super().__init__(
            self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed
        )
