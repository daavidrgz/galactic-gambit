import pygame
from animations.animation import Animation
from constants import TILE_SIZE
from systems.resource_manager import Resource, ResourceManager


class ExplosionAnimaton(Animation):
    def __init__(self, position):
        self.resource_manager = ResourceManager.get_instance()
        frames = self.resource_manager.load_animation(Resource.EXPLOSION)
        scaled_frames = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in frames]
        animation = [(frame, 100) for frame in scaled_frames]
        super().__init__(animation, position)
