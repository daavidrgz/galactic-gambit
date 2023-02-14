from entities.entity import Entity
from utils.direction import Direction


class Projectile(Entity):
    def __init__(self, image, hitbox, initial_pos, speed, direction):
        super().__init__(image, hitbox, initial_pos)
        self.speed = speed
        self.direction = direction

    def update(self, elapsed_time):
        delta_position = Direction.get_displacement(
            self.direction, self.speed, elapsed_time
        )
        self.move(delta_position)
