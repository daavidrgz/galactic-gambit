from scenes.scene_manager import scene_manager
import pygame

from constants import DESIGN_HEIGHT, DESIGN_WIDTH, FADE_TIME


MAX_ALPHA = 255


class Scene:
    def __init__(self):
        self.scene_manager = scene_manager
        self.fade_in()
        self.veil = pygame.Surface((DESIGN_HEIGHT, DESIGN_WIDTH))
        self.complete_animation_callback = None

    def fade_in(self):
        self.progress = 0.0
        self.alpha = 255
        self.direction = -1.0

    def fade_out(self):
        self.progress = 0.0
        self.alpha = 0
        self.direction = 1.0

    def hide_scene(self, callback=None):
        self.complete_animation_callback = callback
        self.fade_out()

    def draw(self, screen):
        self.draw_scene(screen)
        # Fade animation
        self.veil.set_alpha(self.alpha)
        screen.blit(self.veil, (0, 0))

    def draw_scene(self, screen):
        raise NotImplementedError

    def update(self, elapsed_time):
        if self.progress < 1.0:
            self.progress += elapsed_time / FADE_TIME
            self.progress = min(self.progress, 1.0)
            self.alpha += self.direction * (elapsed_time / FADE_TIME) * MAX_ALPHA
            self.alpha = min(self.alpha, MAX_ALPHA)
            self.alpha = max(self.alpha, 0)
        elif self.complete_animation_callback is not None:
            self.complete_animation_callback()
            self.complete_animation_callback = None

        # Ensure values are within bounds

        self.update_scene(elapsed_time)

    def update_scene(self, elapsed_time):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
