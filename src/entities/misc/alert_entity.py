from entities.entity import Entity
from systems.resource_manager import Resource, ResourceManager

import pygame


class AlertEntity(Entity):
    image = ResourceManager().load_image(Resource.ALERT)
    image = pygame.transform.scale(
        image, (image.get_width() * 2, image.get_height() * 2)
    )

    def __init__(self, initial_pos):
        super().__init__(self.image, initial_pos)
        self.timer = 300

    def update(self, elapsed_time):
        self.timer -= elapsed_time
        if self.timer <= 0:
            self.kill()
            return

        self.position -= (0, 0.15 * elapsed_time)

        super().update(elapsed_time)
