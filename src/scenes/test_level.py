import time
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from mechanics.technology.tech_upgrade_system import TechUpgradeSystem
from scenes.level import Level
from generation.base_terrain import BaseTerrain, TerrainType
from generation.generator import BaseGenerator
from scenes.menus.pause_menu import PauseMenu
from systems.resource_manager import Resource, ResourceManager
from entities.living.enemies.test_enemy import TestEnemy
from systems.camera_manager import ScrollableGroup
from scenes.ship_level import ShipGenerator, ShipTerrain
from scenes.director import Director

import pygame


class TestLevel(Level):
    def __init__(self):
        terrain = ShipTerrain()
        generator = ShipGenerator(terrain)
        background_color = (0, 0, 0)
        super().__init__(generator, terrain, background_color)

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
                    Director().switch_scene(TestLevel())
                if event.key == pygame.K_m:
                    upgrade = TechUpgradeSystem.get_instance().get_random_upgrades(1)[0]
                    print(upgrade)
                    if upgrade is not None:
                        self.player.apply_tech_upgrade(upgrade)
                if event.key == pygame.K_n:
                    upgrade = MagicUpgradeSystem.get_instance().get_random_upgrades(1)[
                        0
                    ]
                    print(upgrade)
                    if upgrade is not None:
                        self.player.apply_magical_upgrade(upgrade)
                if event.key == pygame.K_c:
                    self.sound_controller.play_music(Resource.MUSIC_TEST)
                if event.key == pygame.K_v:
                    self.sound_controller.set_music_volume(50)
                if event.key == pygame.K_b:
                    self.sound_controller.play_sound(Resource.SOUND_TEST)
                if event.key == pygame.K_ESCAPE:
                    self.director.push_scene(PauseMenu())

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
