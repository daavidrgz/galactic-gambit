from entities.living.enemies.ranged_enemies.base_ranged_enemy import BaseRangedEnemy
from systems.resource_manager import Resource
from ai.ranged_ai import RangedAI


class MediumRangedEnemy(BaseRangedEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 3
        self.ai = RangedAI(500, 600, 300, 200)
        self.drag = 0.25
        self.speed = 0.9

        self.damage = 1
        self.knockback = 7
        self.projectile_speed = 6
        self.attack_lifetime = 800
        self.reload_speed = 30

        self.walk_right = Resource.RANGED2_WALK_RIGHT
        self.walk_left = Resource.RANGED2_WALK_LEFT
        self.idle_right = Resource.RANGED2_IDLE_RIGHT
        self.idle_left = Resource.RANGED2_IDLE_LEFT
        self.hurt_right = Resource.RANGED2_HURT_RIGHT
        self.hurt_left = Resource.RANGED2_HURT_LEFT
        self.dead_right = Resource.RANGED2_DEAD_RIGHT
        self.dead_left = Resource.RANGED2_DEAD_LEFT

        self.attack_image = Resource.MEDIUM_ENEMY_PROJECTILE

        super().__init__(
            self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed
        )
