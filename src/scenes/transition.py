from scenes.director import Director
from scenes.scene import Scene

import threading
import pygame

class Transition(Scene):
    def __init__(self, transition_to):
        super().__init__()
        self.next_scene = transition_to
        self.done_loading = False
        self.animation_time = 1.0
        self.director = Director()

    def setup(self):
        self.thread = threading.Thread(target=self.next_scene.load)
        self.thread.start()

        self.background = self.director.virtual_screen.copy()
        self.veil = pygame.Surface(self.background.get_size())

    def update(self, elapsed_time):            
        if not self.done_loading and not self.thread.is_alive() and self.animation_time <= 0:
            self.director = Director()

            # Briefly set next scene as active to ensure consistent setup
            self.director.switch_scene(self.next_scene, False)
            self.next_scene.setup()
            self.next_scene.draw(self.background)

            self.director.switch_scene(self, False)
            self.done_loading = True
            self.animation_time = 1.0

        self.animation_time -= elapsed_time / 1000.0

        if self.done_loading and self.animation_time <= 0:
            self.director.switch_scene(self.next_scene, False)

    def handle_events(self, events):
        pass

    def draw(self, screen):
        #TODO: Nicer load animation
        screen.blit(self.background, (0, 0))
        self.veil.set_alpha(255 * self.animation_time if self.done_loading else 255 * (1.0 - self.animation_time))
        screen.blit(self.veil, (0, 0))