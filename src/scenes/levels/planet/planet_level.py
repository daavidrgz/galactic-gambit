from scenes.levels.level import Level
from scenes.director import Director
from scenes.levels.groups import ParallaxGroup
from scenes.levels.planet.planet_generator import PlanetGenerator
from scenes.levels.planet.planet_terrain import PlanetTerrain
from scenes.levels.cave.cave_level import CaveLevel
from scenes.menus.win_menu import WinMenu
from systems.resource_manager import ResourceManager, Resource
from systems.rng_system import RngSystem, Generator
from entities.living.enemies.ranged_enemies.ranged_enemy_1 import RangedEnemy1
from entities.living.enemies.melee_enemies.melee_enemy_1 import MeleeEnemy1

import pygame

from constants.game_constants import TILE_SIZE
from systems.sound_controller import RandomSounds


class PlanetLevel(Level):
    def __init__(self):
        terrain = PlanetTerrain()
        generator = PlanetGenerator(terrain)
        level_music = Resource.PLANET_LEVEL_MUSIC
        player_footsteps = Resource.PLANET_FOOTSTEPS
        self.scattered_sounds = RandomSounds(
            Resource.SCATTERED_PLANET_SOUNDS,
            10000,
        )

        rmgr = ResourceManager()
        dust_sprite = pygame.sprite.Sprite()
        dust_sprite.image = pygame.transform.smoothscale(
            rmgr.load_image(Resource.DUST), (TILE_SIZE * 100.0, TILE_SIZE * 100.0)
        )
        dust_sprite.image.set_alpha(150)
        dust_sprite.rect = dust_sprite.image.get_rect()
        dust_sprite.image_rect = dust_sprite.image.get_rect()
        dust_sprite.x = dust_sprite.y = TILE_SIZE * 128.25
        self.dust = ParallaxGroup((1.5, 1.5), dust_sprite)

        self.next_level = CaveLevel
        super().__init__(
            generator=generator,
            terrain=terrain,
            scene_music=level_music,
            player_footsteps=player_footsteps,
        )

    def setup(self):
        self.scattered_sounds.play()
        super().setup()

        rng = RngSystem().get_rng(Generator.MAP)
        for _ in range(1):
            x = y = -1000
            while (
                not self.terrain.on_ground_point((x, y))
                or (x - 85 * TILE_SIZE) ** 2 + (y - 85 * TILE_SIZE) ** 2
                < (11 * TILE_SIZE) ** 2
            ):
                x, y = rng.randint(0, TILE_SIZE * 171), rng.randint(0, TILE_SIZE * 171)
            enemy_type = rng.randint(0, 1)
            if enemy_type == 0:
                enemy = RangedEnemy1((x, y))
            else:
                enemy = MeleeEnemy1((x, y))
            self.spawn_enemy(enemy)

    def update(self, elapsed_time):
        self.scattered_sounds.update(elapsed_time)
        super().update(elapsed_time)
        self.enemy_group.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(PlanetLevel())
                if event.key == pygame.K_e:
                    Director().switch_scene(WinMenu())

        super().handle_events(events)
