from scenes.levels.level import Level
from scenes.director import Director
from scenes.levels.groups import ParallaxGroup
from scenes.levels.planet.planet_generator import PlanetGenerator
from scenes.levels.planet.planet_terrain import PlanetTerrain
from scenes.levels.cave.cave_level import CaveLevel
from scenes.menus.win_menu import WinMenu
from systems.resource_manager import ResourceManager, Resource
from generation.enemy_spawning import EnemySpawnGroups

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

        self.possible_enemy_spawns = [
            EnemySpawnGroups.PLANET_MELEE,
            EnemySpawnGroups.PLANET_RANGED,
            EnemySpawnGroups.PLANET_MIXED,
            EnemySpawnGroups.PLANET_MIXED_MELEE,
            EnemySpawnGroups.PLANET_MIXED_RANGE,
            EnemySpawnGroups.PLANET_FULL_MIXUP,
            EnemySpawnGroups.PLANET_MELEE_SUPPORT,
            ]
        self.enemy_spawn_level = 35

        super().__init__(
            generator=generator,
            terrain=terrain,
            scene_music=level_music,
            player_footsteps=player_footsteps,
        )

    def setup(self):
        self.scattered_sounds.play()
        super().setup()

    def update(self, elapsed_time):
        self.scattered_sounds.update(elapsed_time)
        super().update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(PlanetLevel())
                if event.key == pygame.K_e:
                    Director().switch_scene(WinMenu())

        super().handle_events(events)
