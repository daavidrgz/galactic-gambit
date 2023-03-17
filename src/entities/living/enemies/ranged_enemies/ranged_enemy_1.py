import numpy as np
from entities.living.enemies.ranged_enemies.base_ranged_enemy import BaseRangedEnemy
from ai.ranged_ai import RangedAI
from systems.resource_manager import Resource, ResourceManager

class RangedEnemy1(BaseRangedEnemy):
    def __init__(self, initial_pos,):
        self.resource_manager = ResourceManager()
        self.facing_vector = np.array([1, 0], dtype=np.float64)

        self.hp = 2
        self.ai = RangedAI(500, 600, 400, 200, 100)
        self.drag = 0.25
        self.speed = 0.7

        self.walk_right = Resource.RANGED1_WALK_RIGHT
        self.walk_left = Resource.RANGED1_WALK_LEFT
        self.idle_right = Resource.RANGED1_IDLE_RIGHT
        self.idle_left = Resource.RANGED1_IDLE_LEFT
        self.hurt_right = Resource.RANGED1_HURT_RIGHT
        self.hurt_left = Resource.RANGED1_HURT_LEFT
        self.dead_right = Resource.RANGED1_DEAD_RIGHT
        self.dead_left = Resource.RANGED1_DEAD_LEFT
        
        super().__init__(self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed)

    def update(self, elapsed_time):
        super().update(elapsed_time, self.walk_right, self.walk_left, self.idle_right, self.idle_left)

    def hit(self, damage, knockback=None):
        super().hit(damage, self.hurt_right, self.hurt_left, knockback)

    def on_death(self):
        super().on_death(self.dead_right, self.dead_left)
