from entities.living.living_entity import LivingEntity
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from scenes.director import Director
from systems.resource_manager import Resource, ResourceManager
from systems.camera_manager import CameraManager
from systems.control_system import ControlSystem, Action

from constants.game_constants import (
    PLAYER_DRAG,
    PLAYER_SPEED,
    DESIGN_FRAMERATE,
    CAMERA_LOOK_AHEAD,
    SPEED_EPSILON,
)

import numpy as np

PIE = np.pi / 8


class Player(LivingEntity):
    def __init__(self, hp, gun, magic_level, initial_pos):
        self.director = Director.get_instance()
        self.control = ControlSystem.get_instance()
        self.camera = CameraManager.get_instance()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()

        self.shoot_cooldown = 0.0
        self.gun = gun
        self.magic_level = magic_level

        self.facing_vector = np.array([1, 0], dtype=np.float64)

        super().__init__(
            Resource.PLAYER_IDLE_DOWN, initial_pos, PLAYER_DRAG, (0, 19, 20), hp
        )

    # Transform the model of the player into the entity
    def from_player_model(player_model, initial_pos):
        hp = player_model.hp
        gun = player_model.gun
        magic_level = player_model.magic_level
        player = Player(hp, gun, magic_level, initial_pos)
        return player

    def setup(self, bullets, on_level_up):
        self.terrain = self.director.get_scene().get_terrain()
        self.camera.set_center(self.get_position())
        self.magic_level.setup(on_level_up)
        self.bullets = bullets
        super().setup()

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.__update_movement(elapsed_units)

        self.__update_animation()
        self.__update_attack(elapsed_time)

        # Camera
        self.camera.set_target_center(
            self.get_position() + self.velocity * CAMERA_LOOK_AHEAD
        )

        super().update(elapsed_time)

    def increase_exp(self, exp):
        self.magic_level.increase_exp(exp)

    def apply_tech_upgrade(self, upgrade):
        upgrade.apply(self.gun)

    def apply_magical_upgrade(self, upgrade):
        self.gun.add_magical_upgrade(upgrade)

    def __get_screen_position(self):
        scrollx, scrolly = self.camera.get_coords()
        x = self.x - scrollx
        y = self.y - scrolly
        return x, y

    def shoot(self, mouse_pos):
        if not self.gun.is_ready():
            return
        shoot_position = (self.x, self.y)
        shoot_direction = np.array(mouse_pos) - np.array(self.__get_screen_position())
        shoot_direction /= np.linalg.norm(shoot_direction)
        new_bullets = self.gun.shoot(shoot_position, shoot_direction)
        self.bullets.add(new_bullets)
        self.increase_exp(10)

    def __update_attack(self, elapsed_time):
        self.gun.update_cooldown(elapsed_time)

        if self.control.is_mouse_pressed():
            self.shoot(self.control.get_mouse_pos())

    def __update_movement(self, elapsed_units):
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

        self.velocity_norm = np.linalg.norm(self.velocity)
        if self.velocity_norm > SPEED_EPSILON:
            self.facing_vector = self.velocity / self.velocity_norm
        else:
            self.velocity = np.zeros(2)
            self.velocity_norm = 0.0

    def __update_animation(self):
        alpha = np.arctan2(self.facing_vector[1], self.facing_vector[0])
        if alpha < 0.0:
            alpha += 2 * np.pi

        if self.velocity_norm > 0.0:
            if alpha > 15 * PIE or alpha < 3 * PIE:
                self.set_animation(Resource.PLAYER_WALK_RIGHT)
            elif alpha < 5 * PIE:
                self.set_animation(Resource.PLAYER_WALK_DOWN)
            elif alpha < 9 * PIE:
                self.set_animation(Resource.PLAYER_WALK_LEFT)
            elif alpha < 11 * PIE:
                self.set_animation(Resource.PLAYER_WALK_UPLEFT)
            elif alpha < 13 * PIE:
                self.set_animation(Resource.PLAYER_WALK_UP)
            else:
                self.set_animation(Resource.PLAYER_WALK_UPRIGHT)

            self.set_speed_multiplier(1.0 + self.velocity_norm / 10.0)
            return

        if alpha > 15 * PIE or alpha < 3 * PIE:
            self.set_animation(Resource.PLAYER_IDLE_RIGHT)
        elif alpha < 5 * PIE:
            self.set_animation(Resource.PLAYER_IDLE_DOWN)
        elif alpha < 9 * PIE:
            self.set_animation(Resource.PLAYER_IDLE_LEFT)
        elif alpha < 11 * PIE:
            self.set_animation(Resource.PLAYER_IDLE_UPLEFT)
        elif alpha < 13 * PIE:
            self.set_animation(Resource.PLAYER_IDLE_UP)
        else:
            self.set_animation(Resource.PLAYER_IDLE_UPRIGHT)

        self.set_speed_multiplier(1.0)
