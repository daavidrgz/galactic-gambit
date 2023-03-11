from scenes.cave_level import CaveLevel
from scenes.level import Level
from generation.tile import Tile
from scenes.director import Director
from generation.generator import BaseGenerator
from systems.camera_manager import ParallaxGroup, ScrollableGroup
from systems.resource_manager import ResourceManager, Resource
from systems.rng_system import RngSystem, Generator
from generation.base_terrain import BaseTerrain, TerrainType
from entities.living.enemies.test_enemy import TestEnemy

import numpy as np
import pygame

from constants import TILE_SIZE


class PlanetGenerator(BaseGenerator):
    def __init__(self, terrain):
        super().__init__((10, 10), (2, 2), terrain)

        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(Resource.PLANET_FLOOR)
        self.floor_spriteD1 = rmgr.load_tile(Resource.PLANET_FLOOR_D1)

        self.wall_sprite_up = rmgr.load_tile(Resource.PLANET_WALL_UP)
        self.wall_sprite_down = rmgr.load_tile(Resource.PLANET_WALL_DOWN)
        self.wall_sprite_left = rmgr.load_tile(Resource.PLANET_WALL_LEFT)
        self.wall_sprite_right = rmgr.load_tile(Resource.PLANET_WALL_RIGHT)
        self.wall_sprite_leftup = rmgr.load_tile(Resource.PLANET_WALL_LEFTUP)
        self.wall_sprite_rightup = rmgr.load_tile(Resource.PLANET_WALL_RIGHTUP)
        self.wall_sprite_leftdown = rmgr.load_tile(Resource.PLANET_WALL_LEFTDOWN)
        self.wall_sprite_rightdown = rmgr.load_tile(Resource.PLANET_WALL_RIGHTDOWN)
        self.wall_sprite_innerleftup = rmgr.load_tile(Resource.PLANET_WALL_INNERLEFTUP)
        self.wall_sprite_innerrightup = rmgr.load_tile(
            Resource.PLANET_WALL_INNERRIGHTUP
        )
        self.wall_sprite_innerleftdown = rmgr.load_tile(
            Resource.PLANET_WALL_INNERLEFTDOWN
        )
        self.wall_sprite_innerrightdown = rmgr.load_tile(
            Resource.PLANET_WALL_INNERRIGHTDOWN
        )

        self.var_offset_x, self.var_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

    def coordinate_transform(self, x, y):
        x -= 85
        y -= 85
        return (np.sqrt(x * x + y * y), np.arctan2(y, x) * 5)

    def get_sprite(self, x, y, surroundings):
        if surroundings[1, 1] == TerrainType.GROUND:
            return self.get_ground_sprite(x, y)

        return self.get_wall_sprite(x, y, surroundings)

    def get_wall_sprite(self, x, y, surroundings):
        if surroundings[2, 1] == TerrainType.GROUND:
            if surroundings[1, 2] == TerrainType.GROUND:
                return self.wall_sprite_leftup
            if surroundings[1, 0] == TerrainType.GROUND:
                return self.wall_sprite_rightup
            return self.wall_sprite_up

        if surroundings[0, 1] == TerrainType.GROUND:
            if surroundings[1, 2] == TerrainType.GROUND:
                return self.wall_sprite_leftdown
            if surroundings[1, 0] == TerrainType.GROUND:
                return self.wall_sprite_rightdown
            return self.wall_sprite_down

        if surroundings[1, 2] == TerrainType.GROUND:
            return self.wall_sprite_left

        if surroundings[1, 0] == TerrainType.GROUND:
            return self.wall_sprite_right

        if surroundings[0, 0] == TerrainType.GROUND:
            return self.wall_sprite_innerrightdown
        if surroundings[0, 2] == TerrainType.GROUND:
            return self.wall_sprite_innerleftdown
        if surroundings[2, 0] == TerrainType.GROUND:
            return self.wall_sprite_innerrightup
        if surroundings[2, 2] == TerrainType.GROUND:
            return self.wall_sprite_innerleftup

        return None

    def get_ground_sprite(self, x, y):
        n = self.noise(x / 60 + self.var_offset_x, y / 60 + self.var_offset_y)

        if n > 0.70:
            return self.floor_spriteD1

        return self.floor_sprite

    def noise_wall_condition(self, n, x, y):
        return n < (x / 114) ** 3


class PlanetTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = []

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(Resource.POLISHED_ANDESITE)
        for x in range(85 - 15, 85 + 16):
            for y in range(85 - 15, 85 + 16):
                distance_sqr = (x//2*2 - 85)**2 + (y//2*2 - 85)**2
                if distance_sqr < 11**2:
                    self.data[y, x] = TerrainType.GROUND
                    self.sprites.add(Tile(x, y, andesite_sprite))
                elif distance_sqr < 12**2:
                    self.starting_tiles.append((x, y))

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 85.5)


class PlanetLevel(Level):
    def __init__(self):
        terrain = PlanetTerrain()
        generator = PlanetGenerator(terrain)
        background_color = tuple(x // 10 for x in (226, 84, 10))

        rmgr = ResourceManager()
        dust_sprite = pygame.sprite.Sprite()
        dust_sprite.image = pygame.transform.smoothscale(
            rmgr.load_image(Resource.DUST), (TILE_SIZE * 100.0, TILE_SIZE * 100.0)
        )
        dust_sprite.image.set_alpha(150)
        dust_sprite.rect = dust_sprite.image.get_rect()
        dust_sprite.image_rect = dust_sprite.image.get_rect()
        dust_sprite.x = dust_sprite.y = TILE_SIZE * 128.25
        self.dust = ParallaxGroup((1.5, 1.5), dust_sprite)

        super().__init__(generator, terrain, background_color)

    def setup(self):
        super().setup()
        rng = RngSystem().get_rng(Generator.MAP)
        for _ in range(20):
            x = y = -1000
            while (
                not self.terrain.on_ground_point((x, y))
                or (x - 85 * TILE_SIZE) ** 2 + (y - 85 * TILE_SIZE) ** 2
                < (11 * TILE_SIZE) ** 2
            ):
                x, y = rng.randint(0, TILE_SIZE * 171), rng.randint(0, TILE_SIZE * 171)
            enemy = TestEnemy((x, y))
            enemy.setup()
            self.enemy_group.add(enemy)

    def draw(self, screen):
        super().draw(screen)

        # for enemy in self.enemy_group.sprites():
        #    marker = pygame.Surface((4,4))
        #    marker.fill((255,0,255))
        #    x = enemy.target[0]
        #    y = enemy.target[1]
        #    from systems.camera_manager import CameraManager
        #    x -= CameraManager().get_coords()[0]
        #    y -= CameraManager().get_coords()[1]
        #    screen.blit(marker, (x-1,y-1,x+2,y+2))

    def update(self, elapsed_time):
        super().update(elapsed_time)
        self.enemy_group.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(CaveLevel())

        super().handle_events(events)
