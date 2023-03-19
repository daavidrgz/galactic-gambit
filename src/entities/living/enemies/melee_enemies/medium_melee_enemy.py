from entities.living.enemies.melee_enemies.base_melee_enemy import BaseMeleeEnemy
from systems.resource_manager import Resource
from ai.melee_ai import MeleeAI


class MediumMeleeEnemy(BaseMeleeEnemy):
    def __init__(
        self,
        initial_pos,
    ):
        self.hp = 6
        self.ai = MeleeAI(300, 500, 100)
        self.drag = 0.25
        self.speed = 1.5

        self.damage = 2
        self.knockback = 10
        self.projectile_speed = 5
        self.attack_lifetime = 100
        self.reload_speed = 40

        self.walk_right = Resource.MELEE2_WALK_RIGHT
        self.walk_left = Resource.MELEE2_WALK_LEFT
        self.idle_right = Resource.MELEE2_IDLE_RIGHT
        self.idle_left = Resource.MELEE2_IDLE_LEFT
        self.hurt_right = Resource.MELEE2_HURT_RIGHT
        self.hurt_left = Resource.MELEE2_HURT_LEFT
        self.dead_right = Resource.MELEE2_DEAD_RIGHT
        self.dead_left = Resource.MELEE2_DEAD_LEFT

        self.attack_image = Resource.LASER

        super().__init__(
            self.hp, initial_pos, self.idle_right, self.ai, self.drag, self.speed
        )
