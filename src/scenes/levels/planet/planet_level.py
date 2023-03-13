from scenes.levels.level import Level
from scenes.director import Director
from scenes.levels.groups import ParallaxGroup
from scenes.levels.planet.planet_generator import PlanetGenerator
from scenes.levels.planet.planet_terrain import PlanetTerrain
from scenes.levels.cave.cave_level import CaveLevel
from systems.resource_manager import ResourceManager, Resource
from systems.rng_system import RngSystem, Generator
from entities.living.enemies.test_enemy import TestEnemy

import pygame

from constants.game_constants import TILE_SIZE


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

        self.next_level = CaveLevel
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
            self.spawn_enemy(enemy)

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
                    Director().switch_scene(PlanetLevel())

        super().handle_events(events)
