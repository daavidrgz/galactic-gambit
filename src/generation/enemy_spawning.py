from systems.rng_system import RngSystem, Generator
from entities.living.enemies.melee_enemies.weak_melee_enemy import WeakMeleeEnemy
from entities.living.enemies.melee_enemies.medium_melee_enemy import MediumMeleeEnemy
from entities.living.enemies.melee_enemies.strong_melee_enemy import StrongMeleeEnemy
from entities.living.enemies.ranged_enemies.weak_ranged_enemy import WeakRangedEnemy
from entities.living.enemies.ranged_enemies.medium_ranged_enemy import MediumRangedEnemy
from entities.living.enemies.ranged_enemies.strong_ranged_enemy import StrongRangedEnemy
from utils.math import manhattan_norm

import numpy as np
from enum import Enum

from constants.game_constants import TILE_SIZE

class EnemySpawnGroups(Enum):
    SHIP_MELEE = (5,
        [WeakMeleeEnemy, WeakMeleeEnemy]
    )
    SHIP_RANGED = (3,
        [WeakRangedEnemy, WeakRangedEnemy]                    
    )
    SHIP_MIXED = (7,
        [WeakRangedEnemy, WeakRangedEnemy, WeakMeleeEnemy]              
    )

    PLANET_MELEE = (7,
        [MediumMeleeEnemy, MediumMeleeEnemy]                
    )
    PLANET_RANGED = (5,
        [MediumRangedEnemy, MediumRangedEnemy]
    )
    PLANET_MIXED = (9,
        [MediumRangedEnemy, MediumRangedEnemy, MediumMeleeEnemy]
    )
    PLANET_MIXED_MELEE = (8,
        [WeakMeleeEnemy, WeakMeleeEnemy, MediumMeleeEnemy]
    )
    PLANET_MIXED_RANGE = (6,
        [WeakRangedEnemy, WeakRangedEnemy, MediumRangedEnemy]
    )
    PLANET_FULL_MIXUP = (11,
        [WeakMeleeEnemy, WeakRangedEnemy, MediumMeleeEnemy, MediumRangedEnemy, MediumRangedEnemy]
    )
    PLANET_MELEE_SUPPORT = (7,
        [MediumMeleeEnemy, WeakRangedEnemy, WeakRangedEnemy]
    )

    CAVE_MELEE = (9,
        [StrongMeleeEnemy, StrongMeleeEnemy]
    )
    CAVE_RANGED = (7,
        [StrongRangedEnemy, StrongRangedEnemy]
    )
    CAVE_MIXED = (13,
        [StrongMeleeEnemy, StrongMeleeEnemy, StrongRangedEnemy]
    )
    CAVE_RANGED_MIX = (6, 
        [MediumRangedEnemy, StrongRangedEnemy]
    )
    CAVE_MELEE_FULL = (9,
        [WeakMeleeEnemy, MediumMeleeEnemy, StrongMeleeEnemy]
    )
    CAVE_MELEE_SUPPORT = (9,
        [WeakRangedEnemy, WeakRangedEnemy, WeakRangedEnemy, StrongMeleeEnemy]
    )
    CAVE_RANGED_SUPPORT = (8,
        [WeakMeleeEnemy, MediumMeleeEnemy, StrongRangedEnemy]
    )

def _spawn_group(level, group, x, y):
    x = (x + 0.5) * TILE_SIZE
    y = (y + 0.5) * TILE_SIZE
    
    for spawn in group:
        enemy = spawn((x, y))
        level.spawn_enemy(enemy)

def _try_spawn_group(level, terrain, group, spawned_positions, rng, start_x, start_y):
    min_distance = 15
    while True:
        x = rng.randrange(terrain.width) 
        y = rng.randrange(terrain.height)

        if not terrain.on_ground_tile((x, y)):
            continue
        if manhattan_norm((x-start_x, y-start_y)) < 15:
            continue

        if min(
            (manhattan_norm((x-sx, y-sy)) for sx, sy in spawned_positions),
            default=np.inf
        ) < min_distance:
            min_distance -= 1
            continue
        
        _spawn_group(level, group, x, y)
        break

def spawn_enemies(level, terrain, possible_groups, desired_level):
    rng = RngSystem().get_rng(Generator.MAP)

    start_x, start_y = terrain.player_starting_position
    start_x //= TILE_SIZE
    start_y //= TILE_SIZE

    current_level = 0
    spawned_positions = []

    while current_level < desired_level:
        group = rng.choice(possible_groups).value
        current_level += group[0]

        _try_spawn_group(level, terrain, group[1], spawned_positions, rng, start_x, start_y)

    return current_level
