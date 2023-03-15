import numpy as np
from entities.living.enemies.base_enemy import BaseEnemy
from ai.melee_ai import MeleeAI
from entities.projectile.enemy_strike import EnemyStrike
from systems.resource_manager import Resource, ResourceManager


class TestMeleeEnemy(BaseEnemy):
    def __init__(self, initial_pos):
        resource_manager = ResourceManager()
        self.ai = MeleeAI(300, 400, 100)
        image = resource_manager.load_image(Resource.PLAYER)
        self.attack_cooldown = 0.0
        super().__init__(2, initial_pos, image, self.ai, 0.25, 1.0)

    def update(self, elapsed_time):
        self.attack_cooldown -= elapsed_time
        super().update(elapsed_time)

    def trigger_attack(self):
        if self.attack_cooldown > 0.0:
            return
        
        self.attack_cooldown = 500

        direction = np.array(self.player.get_position()) - np.array(self.get_position())
        direction /= np.linalg.norm(direction)
        
        position = np.array(self.get_position() - direction * 20)

        new_projectile = EnemyStrike(position, direction)
        self.level.spawn_enemy_bullet(new_projectile)
