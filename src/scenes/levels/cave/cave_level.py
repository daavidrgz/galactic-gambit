from scenes.levels.cave.cave_generator import CaveGenerator
from scenes.levels.cave.cave_terrain import CaveTerrain
from scenes.levels.level import Level
from scenes.director import Director

import pygame


class CaveLevel(Level):
    def __init__(self):
        terrain = CaveTerrain()
        generator = CaveGenerator(terrain)
        background_color = (10, 0, 0)

        super().__init__(generator, terrain, background_color)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(CaveLevel())

        super().handle_events(events)