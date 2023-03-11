from entities.living.living_entity import LivingEntity
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from scenes.director import Director
from systems.resource_manager import Resource, ResourceManager
from systems.camera_manager import CameraManager
from systems.control_system import ControlSystem, Action

from constants import (
    PLAYER_DRAG,
    PLAYER_SPEED,
    DESIGN_FRAMERATE,
    CAMERA_LOOK_AHEAD,
    SPEED_EPSILON,
)

import numpy as np


class Player(LivingEntity):
    def __init__(self, hp, gun, magic_level, initial_pos, bullets):
        self.director = Director.get_instance()
        self.control = ControlSystem.get_instance()
        self.camera = CameraManager.get_instance()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()

        self.bullets = bullets
        self.shoot_cooldown = 0.0
        self.gun = gun
        self.magic_level = magic_level

        self.facing_vector = np.array([1, 0], dtype=np.float64)

        image = ResourceManager().load_image(Resource.PLAYER)
        hitbox = image.get_rect()

        super().__init__(image, hitbox, initial_pos, PLAYER_DRAG, (0, 19, 20), hp)

    # Transform the model of the player into the entity
    def from_player_model(player_model, initial_pos, bullets):
        hp = player_model.hp
        gun = player_model.gun
        magic_level = player_model.magic_level
        player = Player(hp, gun, magic_level, initial_pos, bullets)
        return player

    def setup(self, on_level_up):
        self.terrain = self.director.get_scene().get_terrain()
        self.camera.set_center(self.get_position())
        self.magic_level.setup(on_level_up)

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        # Movement
        move_vector = np.array(
            [
                self.control.is_active_action(Action.RIGHT)
                - self.control.is_active_action(Action.LEFT),
                self.control.is_active_action(Action.DOWN)
                - self.control.is_active_action(Action.UP),
            ],
            dtype=np.float64,
        )

        vector_norm = np.linalg.norm(move_vector)
        if vector_norm > 0.0:
            move_vector /= vector_norm

        self.velocity += move_vector * PLAYER_SPEED * elapsed_units

        velocity_norm = np.linalg.norm(self.velocity)
        if velocity_norm > SPEED_EPSILON:
            self.facing_vector = self.velocity / velocity_norm
        else:
            self.velocity = np.zeros(2)

        # Camera
        self.camera.set_target_center(
            self.get_position() + self.velocity * CAMERA_LOOK_AHEAD
        )

        # Attack
        self.gun.update_cooldown(elapsed_time)

        if self.control.is_active_action(Action.SHOOT):
            self.shoot()

        super().update(elapsed_time)

    def increase_exp(self, exp):
        self.magic_level.increase_exp(exp)

    def apply_tech_upgrade(self, upgrade):
        upgrade.apply(self.gun)

    def apply_magical_upgrade(self, upgrade):
        self.gun.add_magical_upgrade(upgrade)

    def shoot(self):
        if not self.gun.is_ready():
            return
        shoot_position = (self.x, self.y)
        new_bullets = self.gun.shoot(shoot_position, self.facing_vector)
        self.bullets.add(new_bullets)
        self.increase_exp(10)
