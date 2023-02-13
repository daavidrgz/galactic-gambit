from scenes.scene import Scene
from scenes.another_scene import AnotherScene

import pygame
from entities.living.player import Player
from entities.projectile.bullet import Bullet
from constants import DESIGN_WIDTH, DESIGN_HEIGHT
from utils.direction import Direction


class OneScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "One Scene"
        self.player = Player((DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2))
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()

    def draw_scene(self, screen):
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        self.player_group.draw(screen)
        self.bullet_group.draw(screen)

    def update_scene(self, elapsed_time):
        self.player_group.update(elapsed_time)
        self.bullet_group.update(elapsed_time)
        print(f"im in {self.name}")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("switching to another scene")
                    self.scene_manager.push_scene(AnotherScene())
                if event.key == pygame.K_w:
                    x, y = self.player.get_position()
                    new_bullet = Bullet((x, y - 10), 1, Direction.UP)
                    self.bullet_group.add(new_bullet)
                if event.key == pygame.K_a:
                    x, y = self.player.get_position()
                    new_bullet = Bullet((x - 10, y), 1, Direction.LEFT)
                    self.bullet_group.add(new_bullet)
                if event.key == pygame.K_s:
                    x, y = self.player.get_position()
                    new_bullet = Bullet((x, y + 10), 1, Direction.DOWN)
                    self.bullet_group.add(new_bullet)
                if event.key == pygame.K_d:
                    x, y = self.player.get_position()
                    new_bullet = Bullet((x + 10, y), 1, Direction.RIGHT)
                    self.bullet_group.add(new_bullet)
