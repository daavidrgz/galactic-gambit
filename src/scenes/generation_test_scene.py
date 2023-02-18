from scenes.scene import Scene
from generation.generator import BaseGenerator
from control_system import ControlSystem, Actions
from managers.resource_manager import ResourceManager

import pygame
import numpy as np
from constants import TILE_SIZE, DESIGN_WIDTH, DESIGN_HEIGHT

CAMERAX = 114.5 * TILE_SIZE - DESIGN_WIDTH / 2
CAMERAY = 114.5 * TILE_SIZE - DESIGN_HEIGHT / 2

class TestScrollGroup(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            def calculate_rect(r: pygame.Rect):
                copy = r.copy()
                copy.centerx -= CAMERAX
                copy.centery -= CAMERAY
                return copy
            self.spritedict.update(
                zip(sprites, surface.blits((spr.image, calculate_rect(spr.rect)) for spr in sprites))
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

class TestGenerator(BaseGenerator):
    def __init__(self, collide_grp, pass_grp):
        self.resource_manager = ResourceManager.get_instance()
        self.player_sprite = pygame.transform.scale(self.resource_manager.load_image(self.resource_manager.PLAYER), (32, 32))
        self.cobble_sprite = pygame.transform.scale(self.resource_manager.load_image(self.resource_manager.COBBLESTONE), (32, 32))

        super().__init__(np.full((231, 231), False), (114, 114), collide_grp, pass_grp, (10.0, 20.0), (7, 5))

    def get_wall_sprite(self, x, y):
        new_tile = pygame.sprite.Sprite()
        new_tile.image = self.cobble_sprite
        new_tile.rect = new_tile.image.get_rect()
        new_tile.rect.centerx = x * TILE_SIZE + 16
        new_tile.rect.centery = y * TILE_SIZE + 16
        return new_tile
    
    def get_ground_sprite(self, x, y):
        new_tile = pygame.sprite.Sprite()
        new_tile.image = self.player_sprite
        new_tile.rect = new_tile.image.get_rect()
        new_tile.rect.centerx = x * TILE_SIZE + 16
        new_tile.rect.centery = y * TILE_SIZE + 16
        return new_tile

class GenerationScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Generation Test Scene"
        self.ground_group = TestScrollGroup()
        self.wall_group = TestScrollGroup()
        self.control = ControlSystem.get_instance()

    def update(self, elapsed_time):
        global CAMERAX, CAMERAY
        if self.control.is_active_action(Actions.UP   ): CAMERAY -= 5
        if self.control.is_active_action(Actions.DOWN ): CAMERAY += 5
        if self.control.is_active_action(Actions.LEFT ): CAMERAX -= 5
        if self.control.is_active_action(Actions.RIGHT): CAMERAX += 5

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.leave_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ground_group.empty()
                    self.wall_group.empty()
                    import time
                    a = time.time()
                    TestGenerator(self.wall_group, self.ground_group).generate()
                    print(time.time() - a)

    def draw(self, screen):
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        self.ground_group.draw(screen)
        self.wall_group.draw(screen)