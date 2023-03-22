from scenes.levels.level import Level
from scenes.director import Director
from scenes.levels.ship.ship_generator import ShipGenerator
from scenes.levels.ship.ship_terrain import ShipTerrain
from scenes.levels.planet.planet_level import PlanetLevel
from systems.resource_manager import Resource
from systems.rng_system import Generator, RngSystem
from systems.sound_controller import RandomSounds
from generation.enemy_spawning import EnemySpawnGroups

import pygame


class ShipLevel(Level):
    def __init__(self):
        terrain = ShipTerrain()
        generator = ShipGenerator(terrain)

        rng = RngSystem().get_rng(Generator.MAP)
        background = rng.choice(
            [
                Resource.PURPLE_SPACE_BG,
                Resource.ORANGE_SPACE_BG,
                Resource.BLUE_SPACE_BG,
            ]
        )

        level_music = Resource.SHIP_LEVEL_MUSIC
        player_footsteps = Resource.SHIP_FOOTSTEPS
        self.scattered_sounds = RandomSounds(
            Resource.SCATTERED_SHIP_SOUNDS,
            10000,
        )

        self.next_level = PlanetLevel

        self.possible_enemy_spawns = [
            EnemySpawnGroups.SHIP_MELEE,
            EnemySpawnGroups.SHIP_RANGED,
            EnemySpawnGroups.SHIP_MIXED,
        ]
        self.enemy_spawn_level = 25

        super().__init__(
            generator=generator,
            terrain=terrain,
            scene_music=level_music,
            player_footsteps=player_footsteps,
            background=background,
        )

    def update(self, elapsed_time):
        self.scattered_sounds.update(elapsed_time)
        super().update(elapsed_time)

    def setup(self):
        self.scattered_sounds.play()
        super().setup()
