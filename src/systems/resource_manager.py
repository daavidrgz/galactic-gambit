from constants import TILE_SIZE
from utils.singleton import Singleton

import pygame
import os


class ResourceManager(metaclass=Singleton):
    def __init__(self):
        self.resources = {}

        self.BASE_PATH = "assets"

        # Images
        self.SHIP_FLOOR = "sprites/tiles/ship_floor.png"
        self.SHIP_FLOOR_D1 = "sprites/tiles/ship_floord1.png"
        self.SHIP_FLOOR_D2 = "sprites/tiles/ship_floord2.png"
        self.SHIP_FLOOR_D3 = "sprites/tiles/ship_floord3.png"
        self.SHIP_FLOOR_C1 = "sprites/tiles/ship_floorc1.png"
        self.SHIP_FLOOR_C2 = "sprites/tiles/ship_floorc2.png"

        self.PLANET_FLOOR = "sprites/tiles/planet_floor.png"
        self.PLANET_FLOOR_D1 = "sprites/tiles/planet_floord1.png"

        self.DUST = "sprites/dust.png"

        self.PLAYER = "sprites/player.png"
        self.DIRT = "sprites/dirt.png"
        self.COBBLESTONE = "sprites/cobblestone.png"
        self.POLISHED_ANDESITE = "sprites/polished_andesite.png"

        # Sounds (I dont know which ones we will use)
        self.MUSIC_TEST = ("sounds/music_test.ogg", 1)
        self.SOUND_TEST = ("sounds/sound_test.ogg", 1)

        # Coordinates (Will we use them?)

    def load_image(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            fullname = os.path.join(self.BASE_PATH, name)
            try:
                image = pygame.image.load(fullname)
            except (pygame.error):
                print("Error loading image: ", fullname)
                raise SystemExit
            self.resources[name] = image
            return image

    def load_sound(self, sound_name):
        if sound_name in self.resources:
            return self.resources[sound_name]
        else:
            fullname = os.path.join(self.BASE_PATH, sound_name)
            try:
                loaded_sound = pygame.mixer.Sound(fullname)
            except (pygame.error):
                print("Error loading sound: ", fullname)
                raise SystemExit
            self.resources[sound_name] = loaded_sound
            return loaded_sound

    def load_tile(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            fullname = os.path.join(self.BASE_PATH, name)
            try:
                tile = pygame.transform.scale(
                    pygame.image.load(fullname), (TILE_SIZE, TILE_SIZE)
                )
            except (pygame.error):
                print("Error loading tile: ", fullname)
                raise SystemExit
            self.resources[name] = tile
            return tile
