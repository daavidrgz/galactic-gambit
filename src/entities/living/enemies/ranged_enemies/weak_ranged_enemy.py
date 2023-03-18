from entities.living.enemies.ranged_enemies.base_ranged_enemy import BaseRangedEnemy
from systems.resource_manager import Resource
from ai.ranged_ai import RangedAI


class WeakRangedEnemy(BaseRangedEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 3
        self.ai = RangedAI(500, 600, 400, 200)
        self.drag = 0.25
        self.speed = 0.7

        self.damage = 1
        self.knockback = 10
        self.projectile_speed = 8
        self.attack_lifetime = 1000
        self.reload_speed = 100

        self.walk_right = Resource.RANGED1_WALK_RIGHT
        self.walk_left = Resource.RANGED1_WALK_LEFT
        self.idle_right = Resource.RANGED1_IDLE_RIGHT
        self.idle_left = Resource.RANGED1_IDLE_LEFT
        self.hurt_right = Resource.RANGED1_HURT_RIGHT
        self.hurt_left = Resource.RANGED1_HURT_LEFT
        self.dead_right = Resource.RANGED1_DEAD_RIGHT
        self.dead_left = Resource.RANGED1_DEAD_LEFT

        self.attack_image = Resource.LASER

        super().__init__(
            self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed
        )
