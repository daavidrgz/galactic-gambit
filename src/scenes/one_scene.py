from scenes.scene import Scene
from mechanics.technology.upgrade_system import UpgradeSystem
from model.game_model import GameModel
from scenes.another_scene import AnotherScene
from entities.living.player.player import Player
from entities.projectile.bullet import Bullet
from managers.camera_manager import CameraManager, ScrollableGroup
from scenes.generation_test_scene import GenerationScene
from control_system import ControlSystem

import pygame
from constants import DESIGN_WIDTH, DESIGN_HEIGHT

class OneScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "One Scene"
        self.camera_mgr = CameraManager()
        self.bullet_group = ScrollableGroup()

        player_model = GameModel.get_instance().get_player()

        self.player = Player.from_player_model(player_model, (0, 0), self.bullet_group)
        self.player2 = Player.from_player_model(
            player_model, (DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2), self.bullet_group
        )

        self.player_group = ScrollableGroup(self.player)
        self.player2_group = ScrollableGroup(self.player2)

        self.camera_mgr.set_center(self.player.get_position())

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

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("switching to another scene")
                    # update model before leaving scene
                    GameModel.get_instance().update_player(self.player)
                    self.director.push_scene(GenerationScene())
                if event.key == pygame.K_n:
                    print("switching to another scene")
                    self.director.push_scene(AnotherScene())

                if event.key == pygame.K_m:
                    upgrade = UpgradeSystem.get_instance().get_random_upgrade()
                    print(upgrade)
                    if upgrade is not None:
                        self.player.apply_upgrade(upgrade)
