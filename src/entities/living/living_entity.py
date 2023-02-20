from entities.entity import Entity


class LivingEntity(Entity):
    def __init__(self, image, hitbox, initial_pos, hp):
        super().__init__(image, hitbox, initial_pos)
        self.hp = hp

    def hit(self, damage):
        self.hp = max(0.0, self.hp - damage)

    def is_alive(self):
        return self.hp > 0.0
