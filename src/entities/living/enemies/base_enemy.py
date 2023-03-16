import random
from entities.living.living_entity import LivingEntity
from entities.misc.xp_entity import XpEntity
from entities.misc.alert_entity import AlertEntity
from constants.game_constants import DESIGN_FRAMERATE, SPEED_EPSILON
from ai.base_ai import EnemyState

import numpy as np

from systems.resource_manager import Resource


class BaseEnemy(LivingEntity):
    def __init__(self, hp, initial_pos, image, ai, drag, speed):
        self.ai = ai
        self.speed = speed
        self.target = np.zeros(2)
        self.targeting = False
        self.death = False
        self.death_timer = 0
        self.hit_stun = 0

        super().__init__(image, initial_pos, drag, (0, 0, 20), hp)

    def setup(self, level):
        self.player = level.get_player()

        death_sounds = [
            Resource.ALIEN_DEATH_SOUND_01,
            Resource.ALIEN_DEATH_SOUND_02,
            Resource.ALIEN_DEATH_SOUND_03,
        ]
        super().setup(
            level,
            hit_sound=Resource.ALIEN_HIT_SOUND,
            death_sound=random.choice(death_sounds),
        )

    def finish_death_animation(self):
        super().on_death()
        self.kill()
        for _ in range(3):
            self.level.spawn_misc_entity(XpEntity((self.x, self.y), 10))


    def on_death(self):
        self.death_timer = 30
        self.death = True

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        if self.death_timer > 0:
            self.death_timer -= 1
            super().update(elapsed_time)
            return
        
        if self.death:
            self.finish_death_animation()
            return
        
        if self.hit_stun > 0:
            self.hit_stun -= elapsed_units
            super().update(elapsed_time)
            return
        
        self.hit_stun = 0

        self.ai.run(self, self.player, self.terrain, elapsed_time)

        self.__update_movement(elapsed_units)
        super().update(elapsed_time)

    def trigger_attack(self):
        pass

    def alerted(self):
        self.level.spawn_misc_entity(AlertEntity(self.rect.topleft))

    def set_target(self, point):
        if point is None:
            self.targeting = False
            return

        self.target = point
        self.targeting = True

    def get_target(self):
        if not self.targeting:
            return None
        return self.target

    def attack(self):
        pass

    def hit(self, damage, knockback=None):
        if self.hit_stun > 0:
            return
        self.hit_stun = 20
        if self.ai.state == EnemyState.IDLE:
            self.ai.notify()
            self.alerted()
        super().hit(damage, knockback)

    def __update_movement(self, elapsed_units):
        if self.targeting:
            move_vector = self.target - np.array(self.get_position(), dtype=np.float64)
        else:
            move_vector = np.zeros(2)

        vector_norm = np.linalg.norm(move_vector)
        if vector_norm > 0.0:
            move_vector /= vector_norm
            self.facing_vector = move_vector

        self.velocity += move_vector * self.speed * elapsed_units
        self.velocity_norm =  np.linalg.norm(self.velocity)

        if self.velocity_norm > SPEED_EPSILON:
            self.facing_vector = self.velocity / self.velocity_norm
        else:
            self.velocity = np.zeros(2)
            self.velocity_norm = 0.0