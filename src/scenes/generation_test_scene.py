from entities.living.player.player import Player
from model.game_model import GameModel
from scenes.scene import Scene
from generation.generator import BaseGenerator
from systems.control_system import ControlSystem, Actions
from systems.resource_manager import ResourceManager
from systems.camera_manager import CameraManager, ScrollableGroup
from systems.sound_controller import SoundController
from mechanics.technology.upgrade_system import UpgradeSystem

import pygame
import numpy as np
from constants import TILE_SIZE, DESIGN_WIDTH, DESIGN_HEIGHT

CAMERAX = 114.5 * TILE_SIZE - DESIGN_WIDTH / 2
CAMERAY = 114.5 * TILE_SIZE - DESIGN_HEIGHT / 2


class TestGenerator(BaseGenerator):
    def __init__(self, collide_grp, pass_grp):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = pygame.transform.scale(
            self.resource_manager.load_image(self.resource_manager.DIRT), (32, 32)
        )
        self.cobble_sprite = pygame.transform.scale(
            self.resource_manager.load_image(self.resource_manager.COBBLESTONE),
            (32, 32),
        )

        super().__init__(
            np.full((231, 231), False),
            (114, 114),
            collide_grp,
            pass_grp,
            (10.0, 20.0),
            (7, 5),
        )

    def get_wall_sprite(self):
        return self.cobble_sprite

    def get_ground_sprite(self):
        return self.dirt_sprite




# THIS CLASS IS BROKEN DUE TO REFACTOR, USE ONLY AS REFERENCE
class GenerationScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Generation Test Scene"
        self.ground_group = ScrollableGroup()
        self.wall_group = ScrollableGroup()
        self.sound_controller = SoundController.get_instance()
        self.resource_manager = ResourceManager.get_instance()
        self.control = ControlSystem.get_instance()
        self.bullet_group = ScrollableGroup()
        self.camera_mgr = CameraManager()

        player_model = GameModel.get_instance().get_player()

        self.dummy_player = Player.from_player_model(
            player_model, (CAMERAX, CAMERAY), self.bullet_group
        )
        self.dummy_player_group = ScrollableGroup(self.dummy_player)

        self.camera_mgr.set_center(self.dummy_player.get_position())

    def update(self, elapsed_time):
        # TODO: Collision with player & bullet group
        self.dummy_player.update(elapsed_time)
        self.bullet_group.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ground_group.empty()
                    self.wall_group.empty()
                    import time

                    a = time.time()
                    TestGenerator(self.wall_group, self.ground_group).generate()
                    print(time.time() - a)
                if event.key == pygame.K_m:
                    upgrade = UpgradeSystem.get_instance().get_random_upgrade()
                    print(upgrade)
                    if upgrade is not None:
                        self.dummy_player.apply_upgrade(upgrade)
                if event.key == pygame.K_c:
                    self.sound_controller.play_music(self.resource_manager.MUSIC_TEST)
                if event.key == pygame.K_v:
                    self.sound_controller.update_music_volume(50)
                if event.key == pygame.K_b:
                    self.sound_controller.play_sound(self.resource_manager.SOUND_TEST)

    def draw(self, screen):
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        self.ground_group.draw(screen)
        self.wall_group.draw(screen)
        self.bullet_group.draw(screen)
        self.dummy_player_group.draw(screen)
