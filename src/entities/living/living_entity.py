from entities.entity import Entity


class LivingEntity(Entity):
    def __init__(self, image, hitbox, initial_pos, hp):
        super().__init__(image, hitbox, initial_pos)
        self.hp = hp
