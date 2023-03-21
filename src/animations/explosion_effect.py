import pygame
from animations.effect import Effect
from systems.resource_manager import Resource, ResourceManager


class ExplosionEffect(Effect):
    def __init__(self, position):
        self.resource_manager = ResourceManager.get_instance()
        frames = self.resource_manager.load_animation(Resource.EXPLOSION)
        super().__init__(frames, position)
