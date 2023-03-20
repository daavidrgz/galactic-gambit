import numpy as np
from systems.resource_manager import Resource
from entities.living.enemies.base_enemy import BaseEnemy
from entities.projectile.enemy_strike import EnemyStrike

PIH = np.pi / 2


class BaseMeleeEnemy(BaseEnemy):
    def __init__(self, hp, initial_pos, initial_animation, ai, drag, speed):
        self.facing_vector = np.array([1, 0], dtype=np.float64)

        super().__init__(hp, initial_pos, initial_animation, ai, drag, speed)

    def trigger_attack(self):
        if self.attack_timer > 0:
            return

        super().trigger_attack()

        direction = self.player.position - self.position
        direction /= np.linalg.norm(direction)

        position = self.position - direction * 20

        new_projectile = EnemyStrike(
            self.attack_image, position, self.projectile_speed, direction, self.damage, self.knockback, self.attack_lifetime
        )

        self.level.spawn_enemy_bullet(new_projectile)
        self.sound_controller.play_sound(Resource.ALIEN_STRIKE)

    def update_animation(self):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha < 0.0:
            alpha += 2 * np.pi

        if self.velocity_norm > 0.0:
            if alpha > 3 * PIH or alpha < PIH:
                self.set_animation(self.walk_right)
            else:
                self.set_animation(self.walk_left)

            self.set_speed_multiplier(1.0 + self.velocity_norm / 10.0)
            return

        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(self.idle_right)
        else:
            self.set_animation(self.idle_left)

        self.set_speed_multiplier(1.0)

    def hit(self, damage, knockback=None):
        if self.death:
            return
        
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(self.hurt_right)
        else:
            self.set_animation(self.hurt_left)

        super().hit(damage, knockback)

    def on_death(self):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha > 3 * PIH or alpha < PIH:
            self.set_animation(self.dead_right)
        else:
            self.set_animation(self.dead_left)
            
        super().on_death()
