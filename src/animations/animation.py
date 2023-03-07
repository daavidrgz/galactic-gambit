import pygame
import pyganim
from constants import TILE_SIZE

from systems.camera_manager import CameraManager


class Animation(pyganim.PygAnimation):
    def __init__(self, animation, position):
        super().__init__(animation)
        self.position = position

    def play(self):
        super().play()

    def stop(self):
        super().stop()

    def update(self, elapsed_time):
        pass

    def draw(self, screen):
        # TODO: add a ScrollableAnimation :)
        scrollx, scrolly = CameraManager.get_instance().get_coords()
        x, y = self.position
        centerx = round(x) - round(scrollx)
        centery = round(y) - round(scrolly)
        rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        rect.center = (centerx, centery)
        self.blit(screen, rect)

    def is_playing(self):
        return self.isPlaying()

    def is_finished(self):
        return self.isFinished()
