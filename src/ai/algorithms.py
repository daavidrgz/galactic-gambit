import utils.math
import numpy as np

from constants.game_constants import TILE_SIZE, ENEMY_TRACKING_ROTATION


def check_path(terrain, enemy_pos, direction):
    return terrain.on_ground_point(
        enemy_pos + direction * 0.5
    ) and terrain.on_ground_point(enemy_pos + direction * 1.5)


def find_path(current_position, diff_vector, distance, previous_direction, terrain):
    player_direction = diff_vector / distance * TILE_SIZE

    if previous_direction is None:
        previous_direction = player_direction

    if check_path(terrain, current_position, previous_direction):
        while (
            utils.math.square_norm(previous_direction - player_direction)
            > TILE_SIZE**2
        ):
            next_direction = (previous_direction + player_direction) / 2
            next_direction = next_direction / np.linalg.norm(next_direction) * TILE_SIZE
            if check_path(terrain, current_position, next_direction):
                previous_direction = next_direction
            else:
                break
    else:
        for i in range(360 // ENEMY_TRACKING_ROTATION):
            previous_direction = utils.math.rotate_vector(
                previous_direction,
                i * ENEMY_TRACKING_ROTATION * (1 - 2 * (i & 1)),
            )
            if check_path(terrain, current_position, previous_direction):
                break

    return previous_direction


def wander(
    current_position,
    current_target,
    wandering,
    wander_timer,
    terrain,
    rng,
    elapsed_time,
    wander_interval,
):
    target_dist = (
        0
        if current_target is None
        else np.linalg.norm(current_target - current_position)
    )

    if wandering:
        if target_dist > TILE_SIZE and wander_timer > 0:
            wander_timer -= elapsed_time
            return current_target, wandering, wander_timer
        wandering = False
        wander_timer = None

    if wander_timer is None:
        current_target = None
        wander_timer = rng.random() * wander_interval

    wander_timer -= elapsed_time

    if wander_timer <= 0:
        sigma = rng.random() * 360
        direction = utils.math.rotate_vector(np.array((TILE_SIZE / 2, 0.0)), sigma)
        for i in range(rng.randint(1, 20)):
            current_position += direction
            if not terrain.on_ground_point(current_position):
                break
            elif i > 4:
                current_target = current_position
                wander_timer = 5000
                wandering = True

    return current_target, wandering, wander_timer


def search_player(enemy_pos, player_pos, terrain, vision_range, steps=10):
    diff_vector = player_pos - enemy_pos

    distance = np.linalg.norm(diff_vector)

    if distance > vision_range:
        return False
    
    if distance == 0:
        return True

    diff_vector /= steps
    ray_pos = enemy_pos.copy()

    for _ in range(steps):
        ray_pos += diff_vector
        if not terrain.on_ground_point(ray_pos):
            return False
        
    return True
