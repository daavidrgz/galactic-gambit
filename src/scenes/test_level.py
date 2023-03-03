import time
from mechanics.technology.upgrade_system import UpgradeSystem
from scenes.level import Level
from generation.base_terrain import BaseTerrain
from generation.generator import BaseGenerator
from systems.resource_manager import ResourceManager

import pygame


class TestGenerator(BaseGenerator):
    def __init__(self, terrain):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = self.resource_manager.load_tile(self.resource_manager.DIRT)
        self.cobble_sprite = self.resource_manager.load_tile(
            self.resource_manager.COBBLESTONE
        )

        super().__init__(
            (10.0, 20.0),
            (7, 5),
            terrain
        )

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        return self.dirt_sprite

class TestTerrain(BaseTerrain):
    def __init__(self, terrain_size, starting_tile):
        super().__init__(terrain_size, starting_tile)

class TestLevel(Level):
    def __init__(self):
        player_starting_position = (114, 114)
        terrain_size = (231, 231)
        terrain = TestTerrain(terrain_size, player_starting_position)
        generator = TestGenerator(terrain)
        background_color = (0, 0, 0)
        super().__init__(generator, terrain, player_starting_position, background_color)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    a = time.time()
                    self.terrain.clear()
                    self.generator.generate()
                    print(time.time() - a)
                if event.key == pygame.K_m:
                    upgrade = UpgradeSystem.get_instance().get_random_upgrade()
                    print(upgrade)
                    if upgrade is not None:
                        self.player.apply_upgrade(upgrade)
                if event.key == pygame.K_c:
                    self.sound_controller.play_music(self.resource_manager.MUSIC_TEST)
                if event.key == pygame.K_v:
                    self.sound_controller.update_music_volume(50)
                if event.key == pygame.K_b:
                    self.sound_controller.play_sound(self.resource_manager.SOUND_TEST)
