from scenes.fade_example import FadeExample
from scenes.scene import Scene
from scenes.another_scene import AnotherScene

import pygame
from entities.living.player import Player
from constants import DESIGN_WIDTH, DESIGN_HEIGHT


class OneScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "One Scene"
        self.player = Player((DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2))
        self.player_group = pygame.sprite.GroupSingle(self.player)

    def draw_scene(self, screen):
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        self.player_group.draw(screen)

    def update_scene(self, elapsed_time):
        print(f"im in {self.name}")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("switching to another scene")
                    self.scene_manager.push_scene(AnotherScene())
                if event.key == pygame.K_a:
                    print("switching to another scene")
                    self.scene_manager.push_scene(FadeExample())
