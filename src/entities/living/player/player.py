from entities.living.living_entity import LivingEntity
from entities.projectile.bullet import Bullet
from managers.resource_manager import ResourceManager
from control_system import ControlSystem, Actions

from constants import PLAYER_DRAG, PLAYER_SPEED, TARGET_FRAMERATE

import pygame
import numpy as np


class Player(LivingEntity):
    def __init__(self, hp, weapon, magic_level, initial_pos, bullets):
        self.manager = ResourceManager.get_instance()
        self.control = ControlSystem.get_instance()
        self.speed = np.zeros(2)

        self.bullets = bullets
        self.shoot_cooldown = 0.0
        self.weapon = weapon
        self.magic_level = magic_level

        self.facing_vector = np.array([1, 0], dtype=np.float64)

        image = self.manager.load_image(self.manager.PLAYER)
        hitbox = image.get_rect()

        super().__init__(image, hitbox, initial_pos, hp)

    # Transform the model of the player into the entity
    def from_player_model(player_model, initial_pos, bullets):
        hp = player_model.hp
        weapon = player_model.weapon
        magic_level = player_model.magic_level
        player = Player(hp, weapon, magic_level, initial_pos, bullets)
        return player

    def update(self, elapsed_time):

        self.weapon.update_cooldown(elapsed_time)

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

        vector_norm = np.linalg.norm(move_vector)
        if vector_norm > 0.0:
            move_vector /= vector_norm

        self.speed += (
            move_vector * PLAYER_SPEED * elapsed_time * TARGET_FRAMERATE / 1000
        )

        speed_norm = np.linalg.norm(self.speed)
        if speed_norm > 0.0:
            self.facing_vector = self.speed / speed_norm

        self.move(self.speed)
        if self.control.is_active_action(Actions.SHOOT):
            self.shoot()

    def shoot(self):
        if not self.weapon.is_ready():
            return
        shoot_position = (self.x, self.y)
        new_bullets = self.weapon.shoot(shoot_position, self.facing_vector)
        self.bullets.add(new_bullets)
