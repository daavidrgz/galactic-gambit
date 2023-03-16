import numpy as np
from entities.living.enemies.base_enemy import BaseEnemy
from ai.ranged_ai import RangedAI
from entities.projectile.enemy_bullet import EnemyBullet
from systems.resource_manager import Resource, ResourceManager
PIH = np.pi / 2

class TestRangedEnemy(BaseEnemy):
    def __init__(self, initial_pos):
        self.resource_manager = ResourceManager()
        self.facing_vector = np.array([1, 0], dtype=np.float64)
        self.ai = RangedAI(500, 600, 400, 200, 100)

        super().__init__(2, initial_pos, Resource.RANGED2_IDLE_RIGHT, self.ai, 0.25, 0.7)

    def trigger_attack(self):
        direction = np.array(self.player.get_position()) - np.array(self.get_position())
        direction /= np.linalg.norm(direction)
        new_projectile = EnemyBullet(self.get_position(), direction)
        self.level.spawn_enemy_bullet(new_projectile)

    def update(self, elapsed_time):
        super().update(elapsed_time)
        if self.hit_stun > 0:
            return
        if self.death_timer > 0:
            return
        if self.death:
            return
        self.__update_animation()


    def __update_animation(self):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha < 0.0:
            alpha += 2 * np.pi

        if self.velocity_norm > 0.0:
            if alpha > 3 * PIH or alpha < PIH:
                self.set_animation(Resource.RANGED2_WALK_RIGHT)
            else:
                self.set_animation(Resource.RANGED2_WALK_LEFT)

            self.set_speed_multiplier(1.0 + self.velocity_norm / 10.0)
            return

        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(Resource.RANGED2_IDLE_RIGHT)
        else:
            self.set_animation(Resource.RANGED2_IDLE_LEFT)

        self.set_speed_multiplier(1.0)

    def hit(self, damage, knockback=None):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(Resource.RANGED2_HURT_RIGHT)
        else:
            self.set_animation(Resource.RANGED2_HURT_LEFT)
        
        super().hit(damage, knockback)

    def on_death(self):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(Resource.RANGED2_DEAD_RIGHT)
        else:
            self.set_animation(Resource.RANGED2_DEAD_LEFT)
        super().on_death()
