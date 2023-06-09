from entities.entity import Entity
from entities.misc.upgrade_entity import UpgradeEntity
from systems.sound_controller import SoundController
from systems.resource_manager import Resource, ResourceManager
from utils.math import circle_rect_collision

import pygame


class ChestEntity(Entity):
    def __init__(self, initial_pos):
        image = ResourceManager().load_image(Resource.CHEST)
        image = pygame.transform.scale(image, [x*2 for x in image.get_size()])
        super().__init__(image, initial_pos)

        self.open = False

    def setup(self, level):
        self.level = level
        super().setup(level)

    def update(self, elapsed_time):
        if self.open:
            return

        for bullet in self.level.player_bullets:
            if circle_rect_collision((bullet.position[0], bullet.position[1], bullet.size), self.rect):
                bullet.kill()
                self.do_open()

        super().update(elapsed_time)

    def do_open(self):
        if self.open:
            return

        self.open = True
        image = ResourceManager().load_image(Resource.CHEST_OPEN)
        image = pygame.transform.scale(image, [x*2 for x in image.get_size()])
        self.set_image(image)

        sound = SoundController()
        sound.play_sound(Resource.CHEST_OPEN_SOUND)
        sound.play_sound(Resource.ALIEN_HIT_SOUND)
        
        self.level.spawn_misc_entity(UpgradeEntity(self.position))
