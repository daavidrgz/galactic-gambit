from scenes.level import Level
from generation.tile import Tile
from scenes.director import Director
from generation.generator import BaseGenerator
from systems.camera_manager import ParallaxGroup, ScrollableGroup
from systems.resource_manager import ResourceManager
from systems.rng_system import RngSystem, Generator
from generation.base_terrain import BaseTerrain, TerrainType
from entities.living.enemies.test_enemy import TestEnemy

import numpy as np
import pygame

from constants import TILE_SIZE

class PlanetGenerator(BaseGenerator):
    def __init__(self, terrain):
        super().__init__((10,10),(2,2),terrain)

        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(rmgr.PLANET_FLOOR)
        self.floor_spriteD1 = rmgr.load_tile(rmgr.PLANET_FLOOR_D1)
        self.cobble_sprite = rmgr.load_tile(rmgr.COBBLESTONE)

        self.var_offset_x, self.var_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

    def coordinate_transform(self, x, y):
        x -= 85
        y -= 85
        return (np.sqrt(x*x + y*y), np.arctan2(y, x) * 5)

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        n = self.noise(x / 60 + self.var_offset_x, y / 60 + self.var_offset_y)
        
        if n > 0.70: return self.floor_spriteD1

        return self.floor_sprite
    
    def noise_wall_condition(self, n, x, y):
        return n < (x / 114)**3

class PlanetTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = []

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(resource_manager.POLISHED_ANDESITE)
        for x in range(85 - 15, 85 + 16):
            for y in range(85 - 15, 85 + 16):
                distance_sqr = (x - 85)**2 + (y - 85)**2
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
        background_color = (40, 30, 20)

        rmgr = ResourceManager()
        dust_sprite = pygame.sprite.Sprite()
        dust_sprite.image = pygame.transform.smoothscale(rmgr.load_image(rmgr.DUST), (TILE_SIZE * 100.0, TILE_SIZE * 100.0))
        dust_sprite.image.set_alpha(150)
        dust_sprite.rect = dust_sprite.image.get_rect()
        dust_sprite.image_rect = dust_sprite.image.get_rect()
        dust_sprite.x = dust_sprite.y = TILE_SIZE * 128.25
        self.dust = ParallaxGroup((1.5, 1.5), dust_sprite)
        self.enemy_grp = ScrollableGroup()

        super().__init__(generator, terrain, background_color)

    def setup(self):
        super().setup()
        rng = RngSystem().get_rng(Generator.MAP)
        for _ in range(20):
            x = y = -1000
            while not self.terrain.on_ground_point((x, y)) or (x - 85*TILE_SIZE)**2 + (y - 85*TILE_SIZE)**2 < (11*TILE_SIZE)**2:
                x, y = rng.randint(0, TILE_SIZE * 171), rng.randint(0, TILE_SIZE * 171)
            enemy = TestEnemy((x, y))
            enemy.setup()
            self.enemy_grp.add(enemy)

    def draw(self, screen):
        screen.fill(self.background_color)
        self.terrain.draw(screen)
        self.player_group.draw(screen)
        self.enemy_grp.draw(screen)
        self.bullet_group.draw(screen)
        self.dust.draw(screen)
        self.terrain.draw_minimap(screen)
        
        for enemy in self.enemy_grp.sprites():
            marker = pygame.Surface((4,4))
            marker.fill((255,0,255))
            x = enemy.target[0]
            y = enemy.target[1]
            from systems.camera_manager import CameraManager
            x -= CameraManager().get_coords()[0]
            y -= CameraManager().get_coords()[1]
            screen.blit(marker, (x-1,y-1,x+2,y+2))

    def update(self, elapsed_time):
        super().update(elapsed_time)
        self.enemy_grp.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(PlanetLevel())

        super().handle_events(events)