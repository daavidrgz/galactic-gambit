from entities.living.living_entity import LivingEntity
from managers.resource_manager import ResourceManager
from control_system import ControlSystem, Actions

from constants import PLAYER_DRAG, PLAYER_SPEED, TARGET_FRAMERATE

import pygame
import numpy as np


class Player(LivingEntity):
    def __init__(self, initial_pos):
        self.manager = ResourceManager.get_instance()
        self.control = ControlSystem.get_instance()
        self.speed = np.zeros(2)

        image = self.manager.load_image(self.manager.PLAYER)
        hitbox = image.get_rect()
        super().__init__(image, hitbox, initial_pos, 100)

    def update(self, elapsed_time):
        self.speed /= PLAYER_DRAG ** (elapsed_time * TARGET_FRAMERATE / 1000)

        move_vector = np.array(
            [
                self.control.is_active_action(Actions.RIGHT)
                - self.control.is_active_action(Actions.LEFT),
                self.control.is_active_action(Actions.DOWN)
                - self.control.is_active_action(Actions.UP),
            ],
            dtype=np.float64,
        )
        vector_length = np.sqrt(np.sum(move_vector**2))
        if vector_length > 0.0:
            move_vector /= np.sqrt(np.sum(move_vector**2))

        self.speed += (
            move_vector * PLAYER_SPEED * elapsed_time * TARGET_FRAMERATE / 1000
        )
        self.move_absolute_position(self.speed)
