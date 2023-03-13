from scenes.levels.cave.cave_generator import CaveGenerator
from scenes.levels.cave.cave_terrain import CaveTerrain
from scenes.levels.level import Level
from scenes.director import Director
import pygame
from systems.resource_manager import Resource


class CaveLevel(Level):
    def __init__(self):
        terrain = CaveTerrain()
        generator = CaveGenerator(terrain)
        background_color = (10, 0, 0)
        level_music = Resource.CAVE_LEVEL_MUSIC
        from scenes.menus.start_menu import StartMenu

        self.next_level = StartMenu
        super().__init__(generator, terrain, background_color, level_music)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(CaveLevel())

        super().handle_events(events)
