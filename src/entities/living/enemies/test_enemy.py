from entities.living.enemies.base_enemy import BaseEnemy
from ai.melee_ai import MeleeAI
from systems.resource_manager import ResourceManager

class TestEnemy(BaseEnemy):
    def __init__(self, initial_pos):
        self.resource_manager = ResourceManager()
        self.hp = 10
        self.ai = MeleeAI(300, 400, 50)
        image = self.resource_manager.load_image(self.resource_manager.POLISHED_ANDESITE)
        super().__init__(self.hp, initial_pos, image, self.ai)
