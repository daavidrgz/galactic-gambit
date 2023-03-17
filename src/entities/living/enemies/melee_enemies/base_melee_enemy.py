import numpy as np
from entities.living.enemies.base_enemy import BaseEnemy
from ai.melee_ai import MeleeAI
from entities.projectile.enemy_strike import EnemyStrike
PIH = np.pi / 2

class BaseMeleeEnemy(BaseEnemy):
    def __init__(self, hp, initial_pos, initial_animation, ai, drag, speed):
        self.facing_vector = np.array([1, 0], dtype=np.float64)
        self.attack_cooldown = 0.0
        
        super().__init__(hp, initial_pos, initial_animation, ai, drag, speed)

    def trigger_attack(self):
        if self.attack_cooldown > 0.0:
            return
        
        self.attack_cooldown = 500

        direction = np.array(self.player.get_position()) - np.array(self.get_position())
        direction /= np.linalg.norm(direction)
        
        position = np.array(self.get_position() - direction * 20)

        new_projectile = EnemyStrike(position, direction)
        self.level.spawn_enemy_bullet(new_projectile)

    def update(self, elapsed_time, walk_right, walk_left, idle_right, idle_left):
        self.attack_cooldown -= elapsed_time
        super().update(elapsed_time)
        if self.hit_stun > 0:
            return
        if self.death_timer > 0:
            return
        if self.death:
            return
        self.__update_animation(walk_right, walk_left, idle_right, idle_left)


    def __update_animation(self, walk_right, walk_left, idle_right, idle_left):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha < 0.0:
            alpha += 2 * np.pi

        if self.velocity_norm > 0.0:
            if alpha > 3 * PIH or alpha < PIH:
                self.set_animation(walk_right)
            else:
                self.set_animation(walk_left)

            self.set_speed_multiplier(1.0 + self.velocity_norm / 10.0)
            return

        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(idle_right)
        else:
            self.set_animation(idle_left)

        self.set_speed_multiplier(1.0)

    def hit(self, damage, hurt_right, hurt_left, knockback=None):
        if self.death:
            return
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(hurt_right)
        else:
            self.set_animation(hurt_left)
        
        super().hit(damage, knockback)

    def on_death(self, dead_right, dead_left):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(dead_right)
        else:
            self.set_animation(dead_left)
        super().on_death()