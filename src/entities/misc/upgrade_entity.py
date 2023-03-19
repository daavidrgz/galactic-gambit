from entities.entity import Entity
from systems.resource_manager import Resource
from systems.sound_controller import SoundController

import pygame
import numpy as np


class UpgradeEntity(Entity):
    def __init__(self, initial_pos):
        super().__init__(Resource.WRENCH, initial_pos)

        self.velocity = np.zeros(2)
        self.timer = 0

    def setup(self, level):
        super().setup(level)
        self.speed = 0.5
        self.moving = True

    def update(self, elapsed_time):
        if self.moving:
            self.speed -= elapsed_time * 0.001
            self.move((0, -self.speed * elapsed_time))
            if self.speed < -0.35:
                self.moving = False

        if pygame.sprite.collide_rect(self, self.level.player):
            self.pick_up()

        super().update(elapsed_time)

    def pick_up(self):
        sound = SoundController()
        sound.play_sound(Resource.PICKUP_SOUND_1)
        sound.play_sound(Resource.PICKUP_SOUND_2)

        self.level.player_tech_upgrade()
        self.kill()