import pygame
from scenes.another_scene import AnotherScene
from entities.living.player import Player
from entities.projectile.bullet import Bullet
from constants import DESIGN_WIDTH, DESIGN_HEIGHT
from scenes.scrollable_scene import ScrollableScene, ScrollableGroup
from scenes.generation_test_scene import GenerationScene
from control_system import ControlSystem, Actions


class OneScene(ScrollableScene):
    def __init__(self):
        super().__init__()
        self.name = "One Scene"
        self.bullet_group = ScrollableGroup(self.scroll)

        self.player = Player((0, 0), self.bullet_group)
        self.player2 = Player(
            (DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2), self.bullet_group
        )

        self.player_group = ScrollableGroup(self.scroll, self.player)
        self.player2_group = ScrollableGroup(self.scroll, self.player2)

        self.scroll.center_at(self.player)

        self.control = ControlSystem.get_instance()

    def draw(self, screen):
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        self.player_group.draw(screen)
        self.player2_group.draw(screen)
        self.bullet_group.draw(screen)

    def update(self, elapsed_time):
        self.player_group.update(elapsed_time)
        self.bullet_group.update(elapsed_time)

        # if pygame.sprite.groupcollide(
        #     self.player_group, self.player2_group, False, False
        # ):
        #     print("collided")
        # else:
        #     print("not collided")

        # FIXME: Once we know how are we doing camera stuff, make this not update every frame
        # possible solution: player update returns boolean whether it moved or not
        # TODO: This goes here or in scrollable_scene?
        self.scroll.center_at(self.player)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("switching to another scene")
                    self.director.push_scene(GenerationScene())
                if event.key == pygame.K_n:
                    print("switching to another scene")
                    self.director.push_scene(AnotherScene())
