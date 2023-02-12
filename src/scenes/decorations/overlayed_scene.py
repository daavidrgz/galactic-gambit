import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH


BACKGROUND_ALPHA = 128


class OverlayedScene:
    def __init__(self, scene_manager, background_screen, scene):
        self.scene = scene
        self.background_screen = background_screen
        self.scene_manager = scene_manager
        self.veil = pygame.Surface((DESIGN_HEIGHT, DESIGN_WIDTH))
        self.veil.set_alpha(BACKGROUND_ALPHA)

    def draw(self, screen):
        self.background_screen.draw(screen)
        screen.blit(self.veil, (0, 0))
        self.scene.draw(screen)

    def update(self, elapsed_time):
        self.scene.update(elapsed_time)

    def handle_events(self, events):
        self.scene.handle_events(events)
