from entities.living.living_entity import LivingEntity
from entities.projectile.bullet import Bullet
from systems.resource_manager import ResourceManager
from systems.camera_manager import CameraManager
from systems.control_system import ControlSystem, Actions
from scenes.director import Director

from constants import (
    PLAYER_DRAG,
    PLAYER_SPEED,
    DESIGN_FRAMERATE,
    CAMERA_LOOK_AHEAD,
    SPEED_EPSILON,
)

import pygame
import numpy as np
import utils.math


class Player(LivingEntity):
    def __init__(self, hp, gun, magic_level, initial_pos, bullets):
        self.manager = ResourceManager.get_instance()
        self.control = ControlSystem.get_instance()
        self.camera = CameraManager()

        self.bullets = bullets
        self.shoot_cooldown = 0.0
        self.gun = gun
        self.magic_level = magic_level

        self.speed = np.zeros(2)
        self.facing_vector = np.array([1, 0], dtype=np.float64)

        image = self.manager.load_image(self.manager.PLAYER)
        hitbox = image.get_rect()

        super().__init__(image, hitbox, initial_pos, hp)

    # Transform the model of the player into the entity
    def from_player_model(player_model, initial_pos, bullets):
        hp = player_model.hp
        gun = player_model.gun
        magic_level = player_model.magic_level
        player = Player(hp, gun, magic_level, initial_pos, bullets)
        return player

    def setup(self):
        self.scene = Director().get_scene()

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        # Movement
        self.speed -= PLAYER_DRAG * elapsed_units * self.speed

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

        self.speed += move_vector * PLAYER_SPEED * elapsed_units

        speed_norm = np.linalg.norm(self.speed)
        if speed_norm > SPEED_EPSILON:
            self.facing_vector = self.speed / speed_norm
        else:
            self.speed = np.zeros(2)

        # collision_circle = (self.x + self.speed[0], self.y + 19.0 + self.speed[1], 20.0)

        # def collide(_, b):
        #    return utils.math.circle_rect_collision(collision_circle, b.rect)

        # if (
        #    pygame.sprite.spritecollideany(self, self.scene.wall_group, collide)
        #    is not None
        # ):
        #    collision_circle = (self.x, self.y + 19.0 + self.speed[1], 20.0)
        #    if (
        #        pygame.sprite.spritecollideany(self, self.scene.wall_group, collide)
        #        is None
        #    ):
        #        self.speed[0] = 0.0
        #    else:
        #        collision_circle = (self.x + self.speed[0], self.y + 19.0, 20.0)
        #        if (
        #            pygame.sprite.spritecollideany(self, self.scene.wall_group, collide)
        #            is None
        #        ):
        #            self.speed[1] = 0.0
        #        else:
        #            self.speed = np.zeros(2)

        self.move(self.speed * elapsed_units)

        # Camera
        self.camera.set_target_center(
            self.get_position() + self.speed * CAMERA_LOOK_AHEAD
        )

        # Attack
        self.gun.update_cooldown(elapsed_time)

        if self.control.is_active_action(Actions.SHOOT):
            self.shoot()

    def apply_upgrade(self, upgrade):
        upgrade.modify_gun(self.gun)

    def shoot(self):
        if not self.gun.is_ready():
            return
        shoot_position = (self.x, self.y)
        new_bullets = self.gun.shoot(shoot_position, self.facing_vector)
        self.bullets.add(new_bullets)
