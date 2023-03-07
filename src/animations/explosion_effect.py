import pygame
from animations.animation_frame import AnimationFrame
from animations.effect import Effect
from constants import TILE_SIZE
from systems.resource_manager import Resource, ResourceManager


class ExplosionEffect(Effect):
    def __init__(self, position):
        self.resource_manager = ResourceManager.get_instance()
        images = self.resource_manager.load_animation(Resource.EXPLOSION)
        scaled_images = [
            pygame.transform.scale(image, (2 * TILE_SIZE, 2 * TILE_SIZE))
            for image in images
        ]
        frames = [AnimationFrame(image, 50) for image in scaled_images]
        super().__init__(frames, position)

    def on_animation_finished(self):
        self.kill()
