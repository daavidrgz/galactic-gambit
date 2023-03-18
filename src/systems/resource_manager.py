import os
from enum import Enum

import pygame

from animations.animation_frame import AnimationFrame
from constants.game_constants import TILE_SIZE
from utils.singleton import Singleton


class Resource(Enum):

    CROSSHAIR = "sprites/crosshair.png"
    ALERT = "sprites/alert.png"
    PLAYER_PROJECTILE = "sprites/player/projectile.png"
    LASER = "sprites/laser/11.png"
    LASER_ENEMY = "sprites/laser/35.png"

    # Backgrounds
    PLANETS_BG = "sprites/backgrounds/planets-bg.png"
    PURPLE_SPACE_BG = "sprites/backgrounds/purple-space-bg.png"
    BLUE_SPACE_BG = "sprites/backgrounds/blue-space-bg.png"
    ORANGE_SPACE_BG = "sprites/backgrounds/orange-space-bg.png"

    SHIP_END = "sprites/level/ship_end.png"
    SHIP_START = "sprites/level/ship_start.png"
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

    PLANET_END = "sprites/level/planet_end.png"
    PLANET_START = "sprites/level/planet_start.png"
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

    CAVE_START = "sprites/level/cave_start.png"
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

    # Player Sounds
    GET_EXP_SOUND = ("sounds/player/get-exp.wav", 0.4)
    LEVEL_UP_SOUND = ("sounds/player/level-up.mp3", 0.3)
    PLAYER_HIT_SOUND = ("sounds/player/player-hit.mp3", 0.25)
    PLAYER_DEATH_SOUND = ("sounds/player/player-death.mp3", 0.25)

    # Alien sounds
    ALIEN_HIT_SOUND = ("sounds/alien/alien-hit.mp3", 0.25)
    ALIEN_CLOSE_SOUND = ("sounds/alien/alien-close-sound.mp3", 1)
    ALIEN_DEATH_SOUND_01 = ("sounds/alien/alien-death-01.mp3", 0.5)
    ALIEN_DEATH_SOUND_02 = ("sounds/alien/alien-death-02.mp3", 0.5)
    ALIEN_DEATH_SOUND_03 = ("sounds/alien/alien-death-03.mp3", 0.5)

    SCATTERED_SHIP_SOUNDS = [
        ("sounds/ambiance/ship/alien-sound.mp3", 0.5),
        ("sounds/ambiance/ship/far-alien.mp3", 0.25),
        ("sounds/ambiance/ship/signal-emitter.mp3", 0.1),
        ("sounds/ambiance/ship/signal-emitter-alt.mp3", 0.05),
    ]

    SCATTERED_PLANET_SOUNDS = [
        ("sounds/ambiance/planet/wind.mp3", 0.1),
        ("sounds/ambiance/planet/crows.mp3", 0.1),
        ("sounds/ambiance/planet/vulture.mp3", 0.1),
    ]

    SCATTERED_CAVE_SOUNDS = [
        ("sounds/ambiance/cave/water-drop-echo.mp3", 0.3),
        ("sounds/ambiance/cave/water-drops.mp3", 0.7),
        ("sounds/ambiance/cave/water-drops-alt.mp3", 0.7),
    ]

    # Interface sounds
    SELECT_SOUND = ("sounds/interface/select.ogg", 0.4)
    CONFIRM_SOUND = ("sounds/interface/confirm.ogg", 0.3)
    GO_BACK_SOUND = ("sounds/interface/back.ogg", 0.4)
    CONFIRM_ALT_SOUND = ("sounds/interface/confirm_alt.ogg", 0.4)
    GO_BACK_ALT_SOUND = ("sounds/interface/go_back_alt.ogg", 0.6)

    SHIP_FOOTSTEPS = [
        ("sounds/footsteps/ship-footstep-01.mp3", 0.7),
        ("sounds/footsteps/ship-footstep-02.mp3", 0.7),
        ("sounds/footsteps/ship-footstep-03.mp3", 0.7),
        ("sounds/footsteps/ship-footstep-04.mp3", 0.7),
        ("sounds/footsteps/ship-footstep-05.mp3", 0.7),
    ]

    PLANET_FOOTSTEPS = [
        ("sounds/footsteps/planet-footstep-01.mp3", 0.7),
        ("sounds/footsteps/planet-footstep-03.mp3", 0.7),
        ("sounds/footsteps/planet-footstep-04.mp3", 0.7),
        ("sounds/footsteps/planet-footstep-02.mp3", 0.7),
    ]

    CAVE_FOOTSTEPS = [
        ("sounds/footsteps/cave-footstep-01.mp3", 0.7),
        ("sounds/footsteps/cave-footstep-02.mp3", 0.7),
        ("sounds/footsteps/cave-footstep-05.mp3", 0.3),
        ("sounds/footsteps/cave-footstep-03.mp3", 0.7),
        ("sounds/footsteps/cave-footstep-04.mp3", 0.4),
    ]

    LASER_SHOTS = [
        ("sounds/shots/laser-shot-01.wav", 0.8),
    ]

    # Music
    START_MENU_MUSIC = ("music/start_menu_music.mp3", 0.9)
    SHIP_LEVEL_MUSIC = ("music/ship_music.mp3", 0.9)
    PLANET_LEVEL_MUSIC = ("music/planet_music.mp3", 0.9)
    CAVE_LEVEL_MUSIC = ("music/cave_music.mp3", 0.9)
    WIN_MUSIC = ("music/win_music.mp3", 0.9)
    GAME_OVER_MUSIC = ("music/game_over_music.mp3", 0.9)

    # Fonts
    FONT_SM = ("fonts/GalacticaGrid.ttf", 10)
    FONT_MD = ("fonts/GalacticaGrid.ttf", 20)
    FONT_LG = ("fonts/GalacticaGrid.ttf", 40)
    FONT_XL = ("fonts/GalacticaGrid.ttf", 50)

    # Icons
    HEART_ICON = "sprites/icons/heart.png"
    BIGGER_SIZE_ICON = "sprites/icons/bigger.png"
    SNAKE_ICON = "sprites/icons/snake.png"
    WAVEFORM_ICON = "sprites/icons/waveform.png"
    SLOW_AND_FAST_ICON = "sprites/icons/slow-and-fast.png"
    PRISM_ICON = "sprites/icons/prism.png"
    BLACKHOLE_ICON = "sprites/icons/blackhole.png"
    GHOST_ICON = "sprites/icons/ghost.png"
    GHOST_ALT_ICON = "sprites/icons/ghost-alt.png"
    AIM_ICON = "sprites/icons/aim.png"

    TRIPLE_SHOT_ICON = "sprites/icons/triple-shot.png"
    DOUBLE_SHOT_ICON = "sprites/icons/double-shot.png"

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

    RANGED1_IDLE_RIGHT = [
        ("sprites/enemies/ranged/ranged1_idle1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_idle2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_idle3.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_idle4.png", 3, 200, False),
    ]

    RANGED1_IDLE_LEFT = [
        ("sprites/enemies/ranged/ranged1_idle1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_idle2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_idle3.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_idle4.png", 3, 200, True),
    ]

    RANGED1_WALK_RIGHT = [
        ("sprites/enemies/ranged/ranged1_walking1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_walking2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_walking3.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_walking4.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_walking5.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_walking6.png", 3, 200, False),
    ]

    RANGED1_WALK_LEFT = [
        ("sprites/enemies/ranged/ranged1_walking1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_walking2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_walking3.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_walking4.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_walking5.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_walking6.png", 3, 200, True),
    ]

    RANGED1_DEAD_RIGHT = [
        ("sprites/enemies/ranged/ranged1_dead1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_dead2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged1_dead3.png", 3, 200, False),
    ]

    RANGED1_DEAD_LEFT = [
        ("sprites/enemies/ranged/ranged1_dead1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_dead2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged1_dead3.png", 3, 200, True),
    ]

    RANGED1_HURT_RIGHT = [
        ("sprites/enemies/ranged/ranged1_hurt2.png", 3, 200, False),
    ]

    RANGED1_HURT_LEFT = [
        ("sprites/enemies/ranged/ranged1_hurt2.png", 3, 200, True),
    ]

    RANGED2_IDLE_RIGHT = [
        ("sprites/enemies/ranged/ranged2_idle1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_idle2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_idle3.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_idle4.png", 3, 200, False),
    ]

    RANGED2_IDLE_LEFT = [
        ("sprites/enemies/ranged/ranged2_idle1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_idle2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_idle3.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_idle4.png", 3, 200, True),
    ]

    RANGED2_WALK_RIGHT = [
        ("sprites/enemies/ranged/ranged2_walking1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_walking2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_walking3.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_walking4.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_walking5.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_walking6.png", 3, 200, False),
    ]

    RANGED2_WALK_LEFT = [
        ("sprites/enemies/ranged/ranged2_walking1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_walking2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_walking3.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_walking4.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_walking5.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_walking6.png", 3, 200, True),
    ]

    RANGED2_DEAD_RIGHT = [
        ("sprites/enemies/ranged/ranged2_dead1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_dead2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged2_dead3.png", 3, 200, False),
    ]

    RANGED2_DEAD_LEFT = [
        ("sprites/enemies/ranged/ranged2_dead1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_dead2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged2_dead3.png", 3, 200, True),
    ]

    RANGED2_HURT_RIGHT = [
        ("sprites/enemies/ranged/ranged2_hurt2.png", 3, 200, False),
    ]

    RANGED2_HURT_LEFT = [
        ("sprites/enemies/ranged/ranged2_hurt2.png", 3, 200, True),
    ]

    RANGED3_IDLE_RIGHT = [
        ("sprites/enemies/ranged/ranged3_idle1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_idle2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_idle3.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_idle4.png", 3, 200, False),
    ]

    RANGED3_IDLE_LEFT = [
        ("sprites/enemies/ranged/ranged3_idle1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_idle2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_idle3.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_idle4.png", 3, 200, True),
    ]

    RANGED3_WALK_RIGHT = [
        ("sprites/enemies/ranged/ranged3_walking1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_walking2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_walking3.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_walking4.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_walking5.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_walking6.png", 3, 200, False),
    ]

    RANGED3_WALK_LEFT = [
        ("sprites/enemies/ranged/ranged3_walking1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_walking2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_walking3.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_walking4.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_walking5.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_walking6.png", 3, 200, True),
    ]

    RANGED3_DEAD_RIGHT = [
        ("sprites/enemies/ranged/ranged3_dead1.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_dead2.png", 3, 200, False),
        ("sprites/enemies/ranged/ranged3_dead3.png", 3, 200, False),
    ]

    RANGED3_DEAD_LEFT = [
        ("sprites/enemies/ranged/ranged3_dead1.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_dead2.png", 3, 200, True),
        ("sprites/enemies/ranged/ranged3_dead3.png", 3, 200, True),
    ]

    RANGED3_HURT_RIGHT = [
        ("sprites/enemies/ranged/ranged3_hurt2.png", 3, 200, False),
    ]

    RANGED3_HURT_LEFT = [
        ("sprites/enemies/ranged/ranged2_hurt2.png", 3, 200, True),
    ]

    MELEE1_IDLE_RIGHT = [
        ("sprites/enemies/melee/melee1_idle1.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_idle2.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_idle3.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_idle4.png", 3, 200, False),
    ]

    MELEE1_IDLE_LEFT = [
        ("sprites/enemies/melee/melee1_idle1.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_idle2.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_idle3.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_idle4.png", 3, 200, True),
    ]

    MELEE1_WALK_RIGHT = [
        ("sprites/enemies/melee/melee1_walking1.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_walking2.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_walking3.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_walking4.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_walking5.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_walking6.png", 3, 200, False),
    ]

    MELEE1_WALK_LEFT = [
        ("sprites/enemies/melee/melee1_walking1.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_walking2.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_walking3.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_walking4.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_walking5.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_walking6.png", 3, 200, True),
    ]

    MELEE1_DEAD_RIGHT = [
        ("sprites/enemies/melee/melee1_dead1.png", 3, 200, False),
        ("sprites/enemies/melee/melee1_dead2.png", 3, 200, False),
    ]

    MELEE1_DEAD_LEFT = [
        ("sprites/enemies/melee/melee1_dead1.png", 3, 200, True),
        ("sprites/enemies/melee/melee1_dead2.png", 3, 200, True),
    ]

    MELEE1_HURT_RIGHT = [
        ("sprites/enemies/melee/melee1_hurt2.png", 3, 200, False),
    ]

    MELEE1_HURT_LEFT = [
        ("sprites/enemies/melee/melee1_hurt2.png", 3, 200, True),
    ]

    MELEE2_IDLE_RIGHT = [
        ("sprites/enemies/melee/melee2_idle1.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_idle2.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_idle3.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_idle4.png", 3, 200, False),
    ]

    MELEE2_IDLE_LEFT = [
        ("sprites/enemies/melee/melee2_idle1.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_idle2.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_idle3.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_idle4.png", 3, 200, True),
    ]

    MELEE2_WALK_RIGHT = [
        ("sprites/enemies/melee/melee2_walking1.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_walking2.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_walking3.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_walking4.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_walking5.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_walking6.png", 3, 200, False),
    ]

    MELEE2_WALK_LEFT = [
        ("sprites/enemies/melee/melee2_walking1.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_walking2.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_walking3.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_walking4.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_walking5.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_walking6.png", 3, 200, True),
    ]

    MELEE2_DEAD_RIGHT = [
        ("sprites/enemies/melee/melee2_dead1.png", 3, 200, False),
        ("sprites/enemies/melee/melee2_dead2.png", 3, 200, False),
    ]

    MELEE2_DEAD_LEFT = [
        ("sprites/enemies/melee/melee2_dead1.png", 3, 200, True),
        ("sprites/enemies/melee/melee2_dead2.png", 3, 200, True),
    ]

    MELEE2_HURT_RIGHT = [
        ("sprites/enemies/melee/melee2_hurt2.png", 3, 200, False),
    ]

    MELEE2_HURT_LEFT = [
        ("sprites/enemies/melee/melee2_hurt2.png", 3, 200, True),
    ]

    MELEE3_IDLE_RIGHT = [
        ("sprites/enemies/melee/melee3_idle1.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_idle2.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_idle3.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_idle4.png", 3, 200, False),
    ]

    MELEE3_IDLE_LEFT = [
        ("sprites/enemies/melee/melee3_idle1.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_idle2.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_idle3.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_idle4.png", 3, 200, True),
    ]

    MELEE3_WALK_RIGHT = [
        ("sprites/enemies/melee/melee3_walking1.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_walking2.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_walking3.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_walking4.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_walking5.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_walking6.png", 3, 200, False),
    ]

    MELEE3_WALK_LEFT = [
        ("sprites/enemies/melee/melee3_walking1.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_walking2.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_walking3.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_walking4.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_walking5.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_walking6.png", 3, 200, True),
    ]

    MELEE3_DEAD_RIGHT = [
        ("sprites/enemies/melee/melee3_dead1.png", 3, 200, False),
        ("sprites/enemies/melee/melee3_dead2.png", 3, 200, False),
    ]

    MELEE3_DEAD_LEFT = [
        ("sprites/enemies/melee/melee3_dead1.png", 3, 200, True),
        ("sprites/enemies/melee/melee3_dead2.png", 3, 200, True),
    ]

    MELEE3_HURT_RIGHT = [
        ("sprites/enemies/melee/melee3_hurt2.png", 3, 200, False),
    ]

    MELEE3_HURT_LEFT = [
        ("sprites/enemies/melee/melee3_hurt3.png", 3, 200, True),
    ]

    XP = [
        ("sprites/xp/xp_1.png", 2, 50, False),
        ("sprites/xp/xp_2.png", 2, 50, False),
        ("sprites/xp/xp_3.png", 2, 50, False),
        ("sprites/xp/xp_4.png", 2, 50, False),
        ("sprites/xp/xp_5.png", 2, 50, False),
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
