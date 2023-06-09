from entities.living.enemies.ranged_enemies.base_ranged_enemy import BaseRangedEnemy
from systems.resource_manager import Resource
from ai.ranged_ai import RangedAI


class StrongRangedEnemy(BaseRangedEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 3
        self.ai = RangedAI(500, 600, 400, 200)
        self.drag = 0.25
        self.speed = 0.7

        self.damage = 4
        self.knockback = 30
        self.projectile_speed = 25
        self.attack_lifetime = 800
        self.reload_speed = 250

        self.walk_right = Resource.RANGED3_WALK_RIGHT
        self.walk_left = Resource.RANGED3_WALK_LEFT
        self.idle_right = Resource.RANGED3_IDLE_RIGHT
        self.idle_left = Resource.RANGED3_IDLE_LEFT
        self.hurt_right = Resource.RANGED3_HURT_RIGHT
        self.hurt_left = Resource.RANGED3_HURT_LEFT
        self.dead_right = Resource.RANGED3_DEAD_RIGHT
        self.dead_left = Resource.RANGED3_DEAD_LEFT

        self.attack_image = Resource.STRONG_ENEMY_PROJECTILE

        super().__init__(
            self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed
        )
