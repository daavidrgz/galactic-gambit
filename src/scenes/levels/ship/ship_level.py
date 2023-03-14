from scenes.levels.level import Level
from scenes.director import Director
from scenes.levels.ship.ship_generator import ShipGenerator
from scenes.levels.ship.ship_terrain import ShipTerrain
from scenes.levels.planet.planet_level import PlanetLevel
import pygame

from systems.resource_manager import Resource


class ShipLevel(Level):
    def __init__(self):
        terrain = ShipTerrain()
        generator = ShipGenerator(terrain)
        background_color = (0, 0, 0)
        level_music = Resource.SHIP_LEVEL_MUSIC
        player_footsteps = Resource.SHIP_FOOTSTEPS
        self.next_level = PlanetLevel
        super().__init__(
            generator=generator,
            terrain=terrain,
            background_color=background_color,
            scene_music=level_music,
            player_footsteps=player_footsteps,
        )

    def setup(self):
        super().setup()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(ShipLevel())

        super().handle_events(events)
