import numpy as np
from entities.living.enemies.base_enemy import BaseEnemy
from ai.ranged_ai import RangedAI
from constants.game_constants import DESIGN_FRAMERATE, SPEED_EPSILON
from entities.projectile.enemy_bullet import EnemyBullet
from systems.resource_manager import Resource, ResourceManager
from ai.base_ai import EnemyState

PIE = np.pi / 8

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
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.ai.run(self, self.player, self.terrain, elapsed_time)

        self.__update_movement(elapsed_units)
        self.__update_animation()

        super().update(elapsed_time)

    def __update_movement(self, elapsed_units):
        if self.targeting:
            move_vector = self.target - np.array(self.get_position(), dtype=np.float64)
        else:
            move_vector = np.zeros(2)

        vector_norm = np.linalg.norm(move_vector)
        if vector_norm > 0.0:
            move_vector /= vector_norm
            self.facing_vector = move_vector

        self.velocity += move_vector * self.speed * elapsed_units
        self.velocity_norm =  np.linalg.norm(self.velocity)

        if self.velocity_norm > SPEED_EPSILON:
            self.facing_vector = self.velocity / self.velocity_norm
        else:
            self.velocity = np.zeros(2)
            self.velocity_norm = 0.0

    def __update_animation(self):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha < 0.0:
            alpha += 2 * np.pi

        if self.velocity_norm > 0.0:
            if alpha > 15 * PIE or alpha < 3 * PIE:
                self.set_animation(Resource.RANGED2_WALK_RIGHT)
            elif alpha < 9 * PIE:
                self.set_animation(Resource.RANGED2_WALK_LEFT)

            self.set_speed_multiplier(1.0 + self.velocity_norm / 10.0)
            return

        if alpha > 15 * PIE or alpha < 3 * PIE:
            self.set_animation(Resource.RANGED2_IDLE_RIGHT)
        elif alpha < 9 * PIE:
            self.set_animation(Resource.RANGED2_IDLE_LEFT)

        self.set_speed_multiplier(1.0)

    def hit(self, damage, knockback=None):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 15 * PIE or alpha < 3 * PIE:
            self.set_animation(Resource.RANGED2_HURT_RIGHT)
        elif alpha < 9 * PIE:
            self.set_animation(Resource.RANGED2_HURT_LEFT)
        
        if self.ai.state == EnemyState.IDLE:
            self.ai.notify()
        super().hit(damage, knockback)
