from scenes.levels.cave.cave_generator import CaveGenerator
from scenes.levels.cave.cave_terrain import CaveTerrain
from scenes.levels.level import Level
from scenes.director import Director
import pygame
from scenes.menus.win_menu import WinMenu
from systems.resource_manager import Resource
from systems.sound_controller import RandomSounds


class CaveLevel(Level):
    def __init__(self):
        terrain = CaveTerrain()
        generator = CaveGenerator(terrain)
        background_color = (10, 0, 0)
        level_music = Resource.CAVE_LEVEL_MUSIC
        player_footsteps = Resource.CAVE_FOOTSTEPS

        self.scattered_sounds = RandomSounds(
            Resource.SCATTERED_CAVE_SOUNDS,
            5000,
        )
        self.next_level = WinMenu
        super().__init__(
            generator=generator,
            terrain=terrain,
            background_color=background_color,
            scene_music=level_music,
            player_footsteps=player_footsteps,
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
                    Director().switch_scene(CaveLevel())

        super().handle_events(events)
