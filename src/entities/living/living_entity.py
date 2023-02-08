from entities.entity import Entity


class LivingEntity(Entity):
    def __init__(self, image, initial_pos, hp):
        super().__init__(image, initial_pos)
        self.hp = hp
