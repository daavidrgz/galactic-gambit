import pygame
from animations.animation_frame import AnimationFrame
from animations.effect import Effect
from constants.game_constants import TILE_SIZE
from systems.resource_manager import Resource, ResourceManager


class ExplosionEffect(Effect):
    def __init__(self, position):
        self.resource_manager = ResourceManager.get_instance()
        frames = self.resource_manager.load_animation(Resource.EXPLOSION)
        super().__init__(frames, position)

    def on_animation_finished(self):
        self.kill()
