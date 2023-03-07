from enum import Enum
from constants import TILE_SIZE
from utils.singleton import Singleton

import pygame
import os


class Resource(Enum):
    COBBLESTONE = "sprites/cobblestone.png"
    SHIP_FLOOR = "sprites/ship-floor-sm.jpg"
    POLISHED_ANDESITE = "sprites/polished_andesite.png"
    SPACE_BACKGROUND = "sprites/space_bg.png"
    LASER = "sprites/laser/11.png"

    # Sounds (I dont know which ones we will use)
    MUSIC_TEST = ("sounds/music_test.ogg", 1)
    SOUND_TEST = ("sounds/sound_test.ogg", 1)

    # Fonts
    FONT_SM = ("fonts/GalacticaGrid.ttf", 10)
    FONT_MD = ("fonts/GalacticaGrid.ttf", 20)
    FONT_LG = ("fonts/GalacticaGrid.ttf", 40)
    FONT_XL = ("fonts/GalacticaGrid.ttf", 50)

    # Animations
    EXPLOSION = [
        "sprites/effects/explosion/01.png",
        "sprites/effects/explosion/02.png",
        "sprites/effects/explosion/03.png",
        "sprites/effects/explosion/04.png",
        "sprites/effects/explosion/05.png",
        "sprites/effects/explosion/06.png",
        "sprites/effects/explosion/07.png",
    ]

    PLAYER = "sprites/player.png"


# TODO: Initialize beforehand big assets like animations \
# (now there is a micro lag when the animation is first loaded)
class ResourceManager(metaclass=Singleton):
    def __init__(self):
        self.resources = {}
        self.BASE_PATH = "assets"

    def __load_sprite(self, rel_path):
        path = os.path.join(self.BASE_PATH, rel_path)
        try:
            image = pygame.image.load(path)
        except (pygame.error):
            print("Error loading image: ", path)
            raise SystemExit
        return image

    def load_image(self, image_resource):
        if image_resource in self.resources:
            return self.resources[image_resource]
        else:
            image = self.__load_sprite(image_resource.value)
            self.resources[image_resource] = image
            return image

    def load_sound(self, sound_resource):
        if sound_resource in self.resources:
            return self.resources[sound_resource]
        else:
            path = os.path.join(self.BASE_PATH, sound_resource.value[0])
            try:
                loaded_sound = pygame.mixer.Sound(path)
            except (pygame.error):
                print("Error loading sound: ", path)
                raise SystemExit
            self.resources[sound_resource] = loaded_sound
            return loaded_sound

    def load_tile(self, tile_resource):
        if tile_resource in self.resources:
            return self.resources[tile_resource]
        else:
            image = self.__load_sprite(tile_resource.value)
            tile_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            self.resources[tile_resource] = tile_image
            return tile_image

    def load_font(self, font_resource):
        if font_resource in self.resources:
            return self.resources[font_resource]
        else:
            (fontName, fontSize) = font_resource.value
            path = os.path.join(self.BASE_PATH, fontName)
            try:
                font = pygame.font.Font(path, fontSize)
            except (pygame.error):
                print("Error loading font: ", fontName)
                raise SystemExit
            self.resources[font_resource] = font
            return font

    def load_animation(self, animation_resource):
        if animation_resource in self.resources:
            return self.resources[animation_resource]
        else:
            animation = [
                self.__load_sprite(rel_path) for rel_path in animation_resource.value
            ]
            self.resources[animation_resource] = animation
            return animation
