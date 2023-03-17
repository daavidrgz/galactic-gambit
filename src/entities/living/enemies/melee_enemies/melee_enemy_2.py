import numpy as np
from entities.living.enemies.melee_enemies.base_melee_enemy import BaseMeleeEnemy
from ai.melee_ai import MeleeAI
from systems.resource_manager import Resource, ResourceManager

class MeleeEnemy2(BaseMeleeEnemy):
    def __init__(self, initial_pos,):
        self.resource_manager = ResourceManager()

        self.hp = 2
        self.ai = MeleeAI(200, 300, 50)
        self.drag = 0.25
        self.speed = 0.7

        self.walk_right = Resource.MELEE2_WALK_RIGHT
        self.walk_left = Resource.MELEE2_WALK_LEFT
        self.idle_right = Resource.MELEE2_IDLE_RIGHT
        self.idle_left = Resource.MELEE2_IDLE_LEFT
        self.hurt_right = Resource.MELEE2_HURT_RIGHT
        self.hurt_left = Resource.MELEE2_HURT_LEFT
        self.dead_right = Resource.MELEE2_DEAD_RIGHT
        self.dead_left = Resource.MELEE2_DEAD_LEFT

        self.attack_image = Resource.LASER
        
        super().__init__(self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed)

    def trigger_attack(self):
        super().trigger_attack(self.attack_image, self.damage, self.knockback, self.projectile_speed)
    
    def update(self, elapsed_time):
        super().update(elapsed_time, self.walk_right, self.walk_left, self.idle_right, self.idle_left)

    def hit(self, damage, knockback=None):
        super().hit(damage, self.hurt_right, self.hurt_left, knockback)

    def on_death(self):
        super().on_death(self.dead_right, self.dead_left)
