from entities.kinematic_entity import KinematicEntity


class LivingEntity(KinematicEntity):
    def __init__(self, image, initial_pos, drag, collision, hp):
        super().__init__(image, initial_pos, drag, collision)
        self.hp = hp

    def hit(self, damage):
        self.hp = max(0.0, self.hp - damage)

    def is_alive(self):
        return self.hp > 0.0
