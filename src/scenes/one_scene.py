from scenes.scene import Scene
from scenes.another_scene import AnotherScene

import pygame
from entities.living.player import Player
from entities.projectile.bullet import Bullet
from constants import DESIGN_WIDTH, DESIGN_HEIGHT
from scenes.scrollable_scene import ScrollableScene
from utils.direction import Direction


class OneScene(ScrollableScene):
    def __init__(self):
        super().__init__()
        self.name = "One Scene"
        self.player = Player((0, 0))
        self.player2 = Player((DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2))

        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.player2_group = pygame.sprite.GroupSingle(self.player2)

        self.scroll.center_at(self.player)

        self.bullet_group = pygame.sprite.Group()

        self.all_sprites.add(self.player_group)
        self.all_sprites.add(self.player2_group)
        self.all_sprites.add(self.bullet_group)

        # Update relative position of all sprites corresponding to the scroll,
        # since the initial relative position of them is the
        # same as the their global position
        self.update_sprites_relative_position()

    def draw(self, screen):
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        self.player_group.draw(screen)
        self.player2_group.draw(screen)
        self.bullet_group.draw(screen)

    def update(self, elapsed_time):
        self.player_group.update(elapsed_time)
        self.bullet_group.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("switching to another scene")
                    self.director.push_scene(AnotherScene())
                if event.key == pygame.K_w:
                    self.scroll.move_scroll((0, -10))
                    self.is_scroll_modified = True
                    self.player.move_absolute_position((0, -10))
                    # new_bullet = Bullet((x, y - 10), 1, Direction.UP)
                    # self.bullet_group.add(new_bullet)
                if event.key == pygame.K_a:
                    self.scroll.move_scroll((-10, 0))
                    self.is_scroll_modified = True
                    self.player.move_absolute_position((-10, 0))
                    # new_bullet = Bullet((x - 10, y), 1, Direction.LEFT)
                    # self.bullet_group.add(new_bullet)
                if event.key == pygame.K_s:
                    self.scroll.move_scroll((0, 10))
                    self.is_scroll_modified = True
                    self.player.move_absolute_position((0, 10))
                    # new_bullet = Bullet((x, y + 10), 1, Direction.DOWN)
                    # self.bullet_group.add(new_bullet)
                if event.key == pygame.K_d:
                    self.scroll.move_scroll((10, 0))
                    self.is_scroll_modified = True
                    self.player.move_absolute_position((10, 0))
                    # new_bullet = Bullet((x + 10, y), 1, Direction.RIGHT)
                    # self.bullet_group.add(new_bullet)
        self.update_sprites_relative_position()
