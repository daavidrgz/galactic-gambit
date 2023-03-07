from ai.base_ai import BaseAI, EnemyState
from systems.rng_system import RngSystem, Generator

import numpy as np

import utils.math
from constants import TILE_SIZE, ENEMY_TRACKING_ROTATION


class MeleeAI(BaseAI):
    def __init__(self, vision_range, tracking_range, melee_range):
        super().__init__()
        self.vision_range = vision_range
        self.tracking_range = tracking_range
        self.melee_range = melee_range
        self.previous_direction = None
        self.attack_from = None
        self.rng = RngSystem().get_rng(Generator.ENEMIES)

        self.actions[EnemyState.IDLE] = self.idle
        self.actions[EnemyState.PREPARING] = self.preparing
        self.actions[EnemyState.ATTACKING] = self.attack
        self.actions[EnemyState.ALERT] = self.alert

    def idle(self, enemy, player, terrain):
        # Compute distance to player, if the player is in vision range
        # and there's direct line of sight change to PREPARING state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)

        if self.search_player(enemy_pos, player_pos, terrain, self.vision_range):
            self.state = EnemyState.PREPARING
            self.previous_direction = None
            self.attack_from = None
            return

        # Stop following the player
        enemy.set_target(None)

        # TODO: If the distance to the player is too big or
        # there is no line of sight wander around

    def preparing(self, enemy, player, terrain):
        # If we haven't decided a direction from which to attack
        if self.attack_from is None:
            self.attack_from = utils.math.rotate_vector(
                np.array((self.melee_range, 0.0)), self.rng.random() * 360
            )

        # Compute distance to player, if out of tracking range change to ALERT
        # and if in melee range change to ATTACK state
        player_pos = (
            np.array(player.get_position(), dtype=np.float64) + self.attack_from
        )
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.melee_range:
            self.state = EnemyState.ATTACKING
            return
        if distance > self.tracking_range:
            self.state = EnemyState.ALERT
            return

        # Track player and avoid walls
        player_direction = diff_vector / distance * TILE_SIZE

        if self.previous_direction is None:
            self.previous_direction = player_direction

        if self.check_path(terrain, enemy_pos, self.previous_direction):
            while (
                utils.math.square_norm(self.previous_direction - player_direction)
                > TILE_SIZE**2
            ):
                next_direction = (self.previous_direction + player_direction) / 2
                if self.check_path(terrain, enemy_pos, next_direction):
                    self.previous_direction = (
                        self.previous_direction + player_direction
                    ) / 2
                else:
                    break
        else:
            for i in range(360 // ENEMY_TRACKING_ROTATION):
                self.previous_direction = utils.math.rotate_vector(
                    self.previous_direction,
                    i * ENEMY_TRACKING_ROTATION * (1 - 2 * (i & 1)),
                )
                if self.check_path(terrain, enemy_pos, self.previous_direction):
                    break

        enemy.set_target(enemy_pos + self.previous_direction)

    def attack(self, enemy, player, terrain):
        # Compute distance to player, if in attack range attack
        # else change back to PREPARING state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance > self.melee_range:
            self.state = EnemyState.PREPARING
            self.previous_direction = None
            self.attack_from = None
            return

        # Stop following the player
        enemy.set_target(None)

        # Attack player
        enemy.trigger_attack()

    def alert(self, enemy, player, terrain):
        # Compute distance to player, if in tracking range change
        # to PREPARING state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.tracking_range:
            self.state = EnemyState.PREPARING
            self.previous_direction = None
            self.attack_from = None
            return

        # Stop following the player
        enemy.set_target(None)

        # TODO: Moves a lot randomly

    def search_player(self, enemy_pos, player_pos, terrain, vision_range):
        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance <= vision_range and distance > 0:
            # If distance is less than vision range and
            # line of sight change state to PREPARING
            diff_vector /= 10.0
            ray_pos = enemy_pos.copy()

            for _ in range(10):
                ray_pos += diff_vector
                if not terrain.on_ground_point(ray_pos):
                    return False
            else:
                return True

    def check_path(self, terrain, enemy_pos, direction):
        return (terrain.on_ground_point(enemy_pos + direction) 
        and terrain.on_ground_point(enemy_pos + direction * 3))