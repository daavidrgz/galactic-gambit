import pygame

from constants import DESIGN_HEIGHT, DESIGN_WIDTH, FADE_IN_TIME, FADE_OUT_TIME

# We dont need to inherit from Scene since this class will be only
# called from the scene manager itself, so we can just use the
# self reference in the scene manager
class FadeInScene:
    def __init__(self, scene_manager, scene):
        self.scene = scene
        self.scene_manager = scene_manager
        self.alpha = 255
        self.veil = pygame.Surface((DESIGN_HEIGHT, DESIGN_WIDTH))
        self.veil.set_alpha(self.alpha)

    def draw(self, screen):
        self.scene.draw(screen)
        screen.blit(self.veil, (0, 0))

    def update(self, elapsed_time):
        self.alpha -= 255 * elapsed_time / FADE_IN_TIME
        if self.alpha <= 0:
            self.alpha = 0
            self.scene_manager.pop_scene_raw()
        self.veil.set_alpha(self.alpha)

    def handle_events(self, events):
        pass


class FadeOutScene:
    def __init__(self, scene_manager, scene):
        super().__init__()
        self.scene = scene
        self.scene_manager = scene_manager
        self.alpha = 0
        self.veil = pygame.Surface((DESIGN_HEIGHT, DESIGN_WIDTH))
        self.veil.set_alpha(self.alpha)

    def draw(self, screen):
        self.scene.draw(screen)
        screen.blit(self.veil, (0, 0))

    def update(self, elapsed_time):
        self.alpha += 255 * elapsed_time / FADE_OUT_TIME
        if self.alpha >= 255:
            self.alpha = 255
            # Pop scene, since in fade out we should let the fade in scene to appear
            self.scene_manager.pop_scene_raw()
        self.veil.set_alpha(self.alpha)

    def handle_events(self, events):
        pass
