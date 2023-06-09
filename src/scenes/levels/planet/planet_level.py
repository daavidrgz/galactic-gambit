from scenes.levels.level import Level
from scenes.levels.planet.planet_generator import PlanetGenerator
from scenes.levels.planet.planet_terrain import PlanetTerrain
from scenes.levels.cave.cave_level import CaveLevel
from systems.resource_manager import Resource
from generation.enemy_spawning import EnemySpawnGroups
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
