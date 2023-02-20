from entities.entity import Entity
from utils.direction import Direction


class Projectile(Entity):
    def __init__(self, image, hitbox, initial_pos, velocity):
        super().__init__(image, hitbox, initial_pos)

        self.velocity = velocity

    def update(self, elapsed_time):
        delta_position = self.velocity * elapsed_time
        self.move(delta_position)
