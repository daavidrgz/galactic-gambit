from enum import Enum
from constants import TILE_SIZE
from utils.singleton import Singleton

import pygame
import os


class Resource(Enum):
    COBBLESTONE = "sprites/cobblestone.png"
    POLISHED_ANDESITE = "sprites/polished_andesite.png"
    SPACE_BACKGROUND = "sprites/space_bg.png"
    LASER = "sprites/laser/11.png"

    SHIP_FLOOR = "sprites/tiles/ship_floor.png"
    SHIP_FLOOR_D1 = "sprites/tiles/ship_floord1.png"
    SHIP_FLOOR_D2 = "sprites/tiles/ship_floord2.png"
    SHIP_FLOOR_D3 = "sprites/tiles/ship_floord3.png"
    SHIP_FLOOR_C1 = "sprites/tiles/ship_floorc1.png"
    SHIP_FLOOR_C2 = "sprites/tiles/ship_floorc2.png"
    SHIP_WALL_UP = "sprites/tiles/ship_wall_up.png"
    SHIP_WALL_DOWN = "sprites/tiles/ship_wall_down.png"
    SHIP_WALL_LEFT = "sprites/tiles/ship_wall_left.png"
    SHIP_WALL_RIGHT = "sprites/tiles/ship_wall_right.png"
    SHIP_WALL_LEFTUP = "sprites/tiles/ship_wall_leftup.png"
    SHIP_WALL_RIGHTUP = "sprites/tiles/ship_wall_rightup.png"
    SHIP_WALL_LEFTDOWN = "sprites/tiles/ship_wall_leftdown.png"
    SHIP_WALL_RIGHTDOWN = "sprites/tiles/ship_wall_rightdown.png"
    SHIP_WALL_INNERLEFTUP = "sprites/tiles/ship_wall_innerleftup.png"
    SHIP_WALL_INNERRIGHTUP = "sprites/tiles/ship_wall_innerrightup.png"
    SHIP_WALL_INNERLEFTDOWN = "sprites/tiles/ship_wall_innerleftdown.png"
    SHIP_WALL_INNERRIGHTDOWN = "sprites/tiles/ship_wall_innerrightdown.png"

    PLANET_FLOOR = "sprites/tiles/planet_floor.png"
    PLANET_FLOOR_D1 = "sprites/tiles/planet_floord1.png"
    PLANET_WALL_UP = "sprites/tiles/planet_wall_up.png"
    PLANET_WALL_DOWN = "sprites/tiles/planet_wall_down.png"
    PLANET_WALL_LEFT = "sprites/tiles/planet_wall_left.png"
    PLANET_WALL_RIGHT = "sprites/tiles/planet_wall_right.png"
    PLANET_WALL_LEFTUP = "sprites/tiles/planet_wall_leftup.png"
    PLANET_WALL_RIGHTUP = "sprites/tiles/planet_wall_rightup.png"
    PLANET_WALL_LEFTDOWN = "sprites/tiles/planet_wall_leftdown.png"
    PLANET_WALL_RIGHTDOWN = "sprites/tiles/planet_wall_rightdown.png"
    PLANET_WALL_INNERLEFTUP = "sprites/tiles/planet_wall_innerleftup.png"
    PLANET_WALL_INNERRIGHTUP = "sprites/tiles/planet_wall_innerrightup.png"
    PLANET_WALL_INNERLEFTDOWN = "sprites/tiles/planet_wall_innerleftdown.png"
    PLANET_WALL_INNERRIGHTDOWN = "sprites/tiles/planet_wall_innerrightdown.png"

    CAVE_FLOOR = "sprites/tiles/cave_floor.png"
    CAVE_WALL_UP = "sprites/tiles/cave_wall_up.png"
    CAVE_WALL_DOWN = "sprites/tiles/cave_wall_down.png"
    CAVE_WALL_LEFT = "sprites/tiles/cave_wall_left.png"
    CAVE_WALL_RIGHT = "sprites/tiles/cave_wall_right.png"
    CAVE_WALL_LEFTUP = "sprites/tiles/cave_wall_leftup.png"
    CAVE_WALL_RIGHTUP = "sprites/tiles/cave_wall_rightup.png"
    CAVE_WALL_LEFTDOWN = "sprites/tiles/cave_wall_leftdown.png"
    CAVE_WALL_RIGHTDOWN = "sprites/tiles/cave_wall_rightdown.png"
    CAVE_WALL_INNERLEFTUP = "sprites/tiles/cave_wall_innerleftup.png"
    CAVE_WALL_INNERRIGHTUP = "sprites/tiles/cave_wall_innerrightup.png"
    CAVE_WALL_INNERLEFTDOWN = "sprites/tiles/cave_wall_innerleftdown.png"
    CAVE_WALL_INNERRIGHTDOWN = "sprites/tiles/cave_wall_innerrightdown.png"

    DUST = "sprites/dust.png"
    DIRT = "sprites/dirt.png"

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
        tile_identifier = tile_resource.value + "_tile"
        if tile_identifier in self.resources:
            return self.resources[tile_identifier]
        else:
            image = self.__load_sprite(tile_resource.value)
            tile_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            self.resources[tile_identifier] = tile_image
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
