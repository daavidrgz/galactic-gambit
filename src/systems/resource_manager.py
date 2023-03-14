import os
from enum import Enum

import pygame

from animations.animation_frame import AnimationFrame
from constants.game_constants import TILE_SIZE
from utils.singleton import Singleton


class Resource(Enum):
    
    CROSSHAIR = "crosshair.png"
    PLAYER = "sprites/player.png"
    COBBLESTONE = "sprites/cobblestone.png"
    POLISHED_ANDESITE = "sprites/polished_andesite.png"
    SPACE_BACKGROUND = "sprites/space_bg.png"
    LASER = "sprites/laser/11.png"
    LASER_ENEMY = "sprites/laser/35.png"

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

    # Sounds
    LASER_SHOT = ("sounds/laser-shot-alt.mp3", 1)

    # Interface sounds
    SELECT_SOUND = ("sounds/interface/select.ogg", 0.4)
    CONFIRM_SOUND = ("sounds/interface/confirm.ogg", 0.3)
    GO_BACK_SOUND = ("sounds/interface/back.ogg", 0.4)
    CONFIRM_ALT_SOUND = ("sounds/interface/confirm_alt.ogg", 0.6)
    GO_BACK_ALT_SOUND = ("sounds/interface/go_back_alt.ogg", 1)

    SHIP_FOOTSTEPS = [
        ("sounds/ship-footstep-01.mp3", 1),
        ("sounds/ship-footstep-02.mp3", 1),
        ("sounds/ship-footstep-03.mp3", 1),
        ("sounds/ship-footstep-04.mp3", 1),
        ("sounds/ship-footstep-05.mp3", 1),
    ]

    LASER_SHOTS = [
        ("sounds/laser/laser-shot-01.wav", 1),
    ]

    # Music
    START_MENU_MUSIC = ("music/start_menu_music.mp3", 1)
    SHIP_LEVEL_MUSIC = ("music/ship_music.mp3", 1)
    PLANET_LEVEL_MUSIC = ("music/planet_music.mp3", 1)
    CAVE_LEVEL_MUSIC = ("music/cave_music.mp3", 1)
    WIN_MUSIC = ("music/win_music.mp3", 1)

    # Fonts
    FONT_SM = ("fonts/GalacticaGrid.ttf", 10)
    FONT_MD = ("fonts/GalacticaGrid.ttf", 20)
    FONT_LG = ("fonts/GalacticaGrid.ttf", 40)
    FONT_XL = ("fonts/GalacticaGrid.ttf", 50)

    # Icons
    HEART_ICON = "sprites/icons/heart.png"

    # Animations
    EXPLOSION = [
        ("sprites/effects/explosion/01.png", 2, 50, False),
        ("sprites/effects/explosion/02.png", 2, 50, False),
        ("sprites/effects/explosion/03.png", 2, 50, False),
        ("sprites/effects/explosion/04.png", 2, 50, False),
        ("sprites/effects/explosion/05.png", 2, 50, False),
        ("sprites/effects/explosion/06.png", 2, 50, False),
        ("sprites/effects/explosion/07.png", 2, 50, False),
    ]

    PLAYER_IDLE_DOWN = [
        ("sprites/player/player_idle_down1.png", 3, 200, False),
        ("sprites/player/player_idle_down2.png", 3, 200, False),
        ("sprites/player/player_idle_down3.png", 3, 200, False),
        ("sprites/player/player_idle_down4.png", 3, 200, False),
    ]

    PLAYER_IDLE_RIGHT = [
        ("sprites/player/player_idle_side1.png", 3, 200, False),
        ("sprites/player/player_idle_side2.png", 3, 200, False),
        ("sprites/player/player_idle_side3.png", 3, 200, False),
        ("sprites/player/player_idle_side4.png", 3, 200, False),
    ]

    PLAYER_IDLE_LEFT = [
        ("sprites/player/player_idle_side1.png", 3, 200, True),
        ("sprites/player/player_idle_side2.png", 3, 200, True),
        ("sprites/player/player_idle_side3.png", 3, 200, True),
        ("sprites/player/player_idle_side4.png", 3, 200, True),
    ]

    PLAYER_IDLE_UP = [
        ("sprites/player/player_idle_up1.png", 3, 200, False),
        ("sprites/player/player_idle_up2.png", 3, 200, False),
        ("sprites/player/player_idle_up3.png", 3, 200, False),
        ("sprites/player/player_idle_up4.png", 3, 200, False),
    ]

    PLAYER_IDLE_UPRIGHT = [
        ("sprites/player/player_idle_updiag1.png", 3, 200, False),
        ("sprites/player/player_idle_updiag2.png", 3, 200, False),
        ("sprites/player/player_idle_updiag3.png", 3, 200, False),
        ("sprites/player/player_idle_updiag4.png", 3, 200, False),
    ]

    PLAYER_IDLE_UPLEFT = [
        ("sprites/player/player_idle_updiag1.png", 3, 200, True),
        ("sprites/player/player_idle_updiag2.png", 3, 200, True),
        ("sprites/player/player_idle_updiag3.png", 3, 200, True),
        ("sprites/player/player_idle_updiag4.png", 3, 200, True),
    ]

    PLAYER_WALK_DOWN = [
        ("sprites/player/player_walk_down1.png", 3, 200, False),
        ("sprites/player/player_walk_down2.png", 3, 200, False),
        ("sprites/player/player_walk_down3.png", 3, 200, False),
        ("sprites/player/player_walk_down4.png", 3, 200, False),
        ("sprites/player/player_walk_down5.png", 3, 200, False),
        ("sprites/player/player_walk_down6.png", 3, 200, False),
    ]

    PLAYER_WALK_RIGHT = [
        ("sprites/player/player_walk_side1.png", 3, 200, False),
        ("sprites/player/player_walk_side2.png", 3, 200, False),
        ("sprites/player/player_walk_side3.png", 3, 200, False),
        ("sprites/player/player_walk_side4.png", 3, 200, False),
        ("sprites/player/player_walk_side5.png", 3, 200, False),
        ("sprites/player/player_walk_side6.png", 3, 200, False),
    ]

    PLAYER_WALK_LEFT = [
        ("sprites/player/player_walk_side1.png", 3, 200, True),
        ("sprites/player/player_walk_side2.png", 3, 200, True),
        ("sprites/player/player_walk_side3.png", 3, 200, True),
        ("sprites/player/player_walk_side4.png", 3, 200, True),
        ("sprites/player/player_walk_side5.png", 3, 200, True),
        ("sprites/player/player_walk_side6.png", 3, 200, True),
    ]

    PLAYER_WALK_UP = [
        ("sprites/player/player_walk_up1.png", 3, 200, False),
        ("sprites/player/player_walk_up2.png", 3, 200, False),
        ("sprites/player/player_walk_up3.png", 3, 200, False),
        ("sprites/player/player_walk_up4.png", 3, 200, False),
        ("sprites/player/player_walk_up5.png", 3, 200, False),
        ("sprites/player/player_walk_up6.png", 3, 200, False),
    ]

    PLAYER_WALK_UPRIGHT = [
        ("sprites/player/player_walk_updiag1.png", 3, 200, False),
        ("sprites/player/player_walk_updiag2.png", 3, 200, False),
        ("sprites/player/player_walk_updiag3.png", 3, 200, False),
        ("sprites/player/player_walk_updiag4.png", 3, 200, False),
        ("sprites/player/player_walk_updiag5.png", 3, 200, False),
        ("sprites/player/player_walk_updiag6.png", 3, 200, False),
    ]

    PLAYER_WALK_UPLEFT = [
        ("sprites/player/player_walk_updiag1.png", 3, 200, True),
        ("sprites/player/player_walk_updiag2.png", 3, 200, True),
        ("sprites/player/player_walk_updiag3.png", 3, 200, True),
        ("sprites/player/player_walk_updiag4.png", 3, 200, True),
        ("sprites/player/player_walk_updiag5.png", 3, 200, True),
        ("sprites/player/player_walk_updiag6.png", 3, 200, True),
    ]


# TODO: Initialize beforehand big assets like animations \
# (now there is a micro lag when the animation is first loaded)
class ResourceManager(metaclass=Singleton):
    def __init__(self):
        self.resources = {}
        self.BASE_PATH = "assets"

    def __load_sprite(self, rel_path, scale=None, flip=None):
        path = os.path.join(self.BASE_PATH, rel_path)
        try:
            image = pygame.image.load(path)
            if flip is not None and flip:
                image = pygame.transform.flip(image, True, False)
            if scale is not None:
                image = pygame.transform.scale(
                    image, (image.get_width() * scale, image.get_height() * scale)
                )
        except (pygame.error):
            print("Error loading image: ", path)
            raise SystemExit
        return image

    def __load_sound(self, rel_path):
        path = os.path.join(self.BASE_PATH, rel_path)
        try:
            loaded_sound = pygame.mixer.Sound(path)
        except (pygame.error):
            print("Error loading sound: ", path)
            raise SystemExit
        return loaded_sound

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
            loaded_sound = self.__load_sound(sound_resource.value[0])
            self.resources[sound_resource] = loaded_sound
            return loaded_sound

    def load_sounds(self, sounds_resource):
        if sounds_resource in self.resources:
            return self.resources[sounds_resource]
        else:
            sounds = []
            for sound_resource in sounds_resource.value:
                loaded_sound = self.__load_sound(sound_resource[0])
                sounds.append((loaded_sound, sound_resource[1]))
            self.resources[sounds_resource] = sounds
            return sounds

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
                AnimationFrame(self.__load_sprite(rel_path, scale, flip), duration)
                for rel_path, scale, duration, flip in animation_resource.value
            ]
            self.resources[animation_resource] = animation
            return animation
