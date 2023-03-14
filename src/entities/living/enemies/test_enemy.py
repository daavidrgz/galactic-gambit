import numpy as np
from entities.living.enemies.base_enemy import BaseEnemy
from ai.melee_ai import MeleeAI
from entities.living.hp import Hp
from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager


class TestEnemy(BaseEnemy):
    def __init__(self, initial_pos):
        self.resource_manager = ResourceManager()
        self.ai = MeleeAI(300, 400, 50)
        image = self.resource_manager.load_image(Resource.POLISHED_ANDESITE)
        super().__init__(2, initial_pos, image, self.ai)

    # TODO: think of a melee attack
    def trigger_attack(self):
        direction = np.array(self.player.get_position()) - np.array(self.get_position())
        direction /= np.linalg.norm(direction)
        image = self.resource_manager.load_image(Resource.LASER)
        new_projectile = Projectile(image, self.get_position(), 100, direction, 1)
        self.bullets.add(new_projectile)
