from constants import TILE_SIZE
from utils.singleton import Singleton

import pygame
import os


class ResourceManager(metaclass=Singleton):
    def __init__(self):
        self.resources = {}

        self.BASE_PATH = "assets"

        # Images
        self.PLAYER = "sprites/player.png"
        self.COBBLESTONE = "sprites/cobblestone.png"
        self.DIRT = "sprites/dirt.png"
        self.POLISHED_ANDESITE = "sprites/polished_andesite.png"
        self.SPACE_BACKGROUND = "sprites/space_bg.png"
        self.LASER = "sprites/laser/11.png"

        # Sounds (I dont know which ones we will use)
        self.MUSIC_TEST = ("sounds/music_test.ogg", 1)
        self.SOUND_TEST = ("sounds/sound_test.ogg", 1)

        # Fonts
        self.FONT_SM = ("fonts/GalacticaGrid.ttf", 10)
        self.FONT_MD = ("fonts/GalacticaGrid.ttf", 20)
        self.FONT_LG = ("fonts/GalacticaGrid.ttf", 40)
        self.FONT_XL = ("fonts/GalacticaGrid.ttf", 50)

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

    def load_font(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            (fontName, fontSize) = name
            fullFontName = os.path.join(self.BASE_PATH, fontName)
            try:
                font = pygame.font.Font(fullFontName, fontSize)
            except (pygame.error):
                print("Error loading font: ", fontName)
                raise SystemExit
            self.resources[name] = font
            return font
