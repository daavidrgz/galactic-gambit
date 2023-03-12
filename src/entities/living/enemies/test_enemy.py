from entities.living.enemies.base_enemy import BaseEnemy
from ai.melee_ai import MeleeAI
from entities.living.hp import Hp
from systems.resource_manager import Resource, ResourceManager


class TestEnemy(BaseEnemy):
    def __init__(self, initial_pos):
        self.resource_manager = ResourceManager()
        self.hp = Hp(10)
        self.ai = MeleeAI(300, 400, 50)
        image = self.resource_manager.load_image(Resource.POLISHED_ANDESITE)
        super().__init__(self.hp, initial_pos, image, self.ai)
