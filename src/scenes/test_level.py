import time
from mechanics.magic.magic_upgrade import DoubleSize, ShrinkAndGrow, SlowAndFast, Woobly
from mechanics.technology.tech_upgrade_system import TechUpgradeSystem
from scenes.level import Level
from generation.base_terrain import BaseTerrain, TerrainType
from generation.generator import BaseGenerator
from systems.resource_manager import ResourceManager
from entities.living.enemies.test_enemy import TestEnemy
from systems.camera_manager import ScrollableGroup

import pygame
import numpy as np


class TestGenerator(BaseGenerator):
    def __init__(self, terrain):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = self.resource_manager.load_tile(self.resource_manager.DIRT)
        self.cobble_sprite = self.resource_manager.load_tile(
            self.resource_manager.COBBLESTONE
        )

        super().__init__((10.0, 20.0), (7, 5), terrain)

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        return self.dirt_sprite


class TestTerrain(BaseTerrain):
    def __init__(self, terrain_size, starting_tile):
        data = np.full(
            tuple(x - 2 for x in terrain_size), TerrainType.NONE, dtype=np.int16
        )
        data = np.pad(
            data, ((1, 1), (1, 1)), mode="constant", constant_values=TerrainType.BOUND
        )
        super().__init__(data, starting_tile)


class TestLevel(Level):
    def __init__(self):
        player_starting_position = (114, 114)
        terrain_size = (231, 231)
        terrain = TestTerrain(terrain_size, player_starting_position)
        generator = TestGenerator(terrain)
        background_color = (0, 0, 0)
        super().__init__(generator, terrain, player_starting_position, background_color)

        self.test_enemy_0 = TestEnemy((124 * 32, 126 * 32))
        self.test_enemy_1 = TestEnemy((124 * 32, 127 * 32))
        self.test_enemy_2 = TestEnemy((124 * 32, 128 * 32))
        self.test_enemy_3 = TestEnemy((124 * 32, 129 * 32))
        self.test_enemy_4 = TestEnemy((125 * 32, 126 * 32))
        self.test_enemy_5 = TestEnemy((125 * 32, 127 * 32))
        self.test_enemy_6 = TestEnemy((125 * 32, 128 * 32))
        self.test_enemy_7 = TestEnemy((125 * 32, 129 * 32))
        self.test_enemy_8 = TestEnemy((123 * 32, 126 * 32))
        self.test_enemy_9 = TestEnemy((123 * 32, 127 * 32))
        self.enemy_grp = ScrollableGroup(
            self.test_enemy_0,
            self.test_enemy_1,
            self.test_enemy_2,
            self.test_enemy_3,
            self.test_enemy_4,
            self.test_enemy_5,
            self.test_enemy_6,
            self.test_enemy_7,
            self.test_enemy_8,
            self.test_enemy_9,
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    a = time.time()
                    self.terrain.clear()
                    self.generator.generate()
                    print(time.time() - a)
                if event.key == pygame.K_m:
                    upgrade = TechUpgradeSystem.get_instance().get_random_upgrade()
                    print(upgrade)
                    if upgrade is not None:
                        self.player.apply_tech_upgrade(upgrade)
                if event.key == pygame.K_c:
                    self.sound_controller.play_music(self.resource_manager.MUSIC_TEST)
                if event.key == pygame.K_v:
                    self.sound_controller.update_music_volume(50)
                if event.key == pygame.K_b:
                    self.sound_controller.play_sound(self.resource_manager.SOUND_TEST)
                if event.key == pygame.K_n:
                    self.player.apply_magical_upgrade(SlowAndFast)

    def setup(self):
        super().setup()
        for enemy in self.enemy_grp:
            enemy.setup()
        # self.test_enemy.setup()

    def update(self, elapsed_time):
        super().update(elapsed_time)
        self.enemy_grp.update(elapsed_time)
        # self.test_enemy.update(elapsed_time)

    def draw(self, screen):
        super().draw(screen)
        self.enemy_grp.draw(screen)
