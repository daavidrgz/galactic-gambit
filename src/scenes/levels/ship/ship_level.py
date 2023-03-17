from scenes.levels.level import Level
from scenes.director import Director
from scenes.levels.ship.ship_generator import ShipGenerator
from scenes.levels.ship.ship_terrain import ShipTerrain
from scenes.levels.planet.planet_level import PlanetLevel
import pygame

from systems.resource_manager import Resource
from systems.rng_system import Generator, RngSystem
from systems.sound_controller import RandomSounds


class ShipLevel(Level):
    def __init__(self):
        terrain = ShipTerrain()
        generator = ShipGenerator(terrain)

        possible_backgrounds = [
            Resource.PURPLE_SPACE_BG,
            Resource.ORANGE_SPACE_BG,
            Resource.BLUE_SPACE_BG,
        ]
        background = RngSystem().get_rng(Generator.MAP).choice(possible_backgrounds)
        level_music = Resource.SHIP_LEVEL_MUSIC
        player_footsteps = Resource.SHIP_FOOTSTEPS

        self.scattered_sounds = RandomSounds(
            Resource.SCATTERED_SHIP_SOUNDS,
            10000,
        )
        self.next_level = PlanetLevel
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

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(ShipLevel())

        super().handle_events(events)
