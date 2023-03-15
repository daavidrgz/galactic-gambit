import numpy as np
from entities.living.enemies.base_enemy import BaseEnemy
from ai.melee_ai import MeleeAI
from ai.ranged_ai import RangedAI
from entities.projectile.enemy_bullet import EnemyBullet
from systems.resource_manager import Resource, ResourceManager


class TestRangedEnemy(BaseEnemy):
    def __init__(self, initial_pos):
        self.resource_manager = ResourceManager()
        self.ai = RangedAI(500, 600, 400, 200, 100)
        image = self.resource_manager.load_image(Resource.PLAYER)
        super().__init__(2, initial_pos, image, self.ai, 0.25, 0.7)

    def trigger_attack(self):
        direction = np.array(self.player.get_position()) - np.array(self.get_position())
        direction /= np.linalg.norm(direction)
        new_projectile = EnemyBullet(self.get_position(), direction)
        self.level.spawn_enemy_bullet(new_projectile)
