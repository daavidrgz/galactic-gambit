import math

import numpy as np
from mechanics.weapons.weapon import Weapon


class SpreadWeapon(Weapon):
    def __init__(self, damage, cooldown, bullet_speed, gun_offset, spread, n_bullets):
        super().__init__(
            damage=50,
            cooldown=500,
            bullet_speed=0.7,
            gun_offset=30,
        )
        # Angle for spread.
        # For example 30 degrees of spread means +-15 degrees of maximum angle offset from initial angle.
        self.spread = spread
        self.n_bullets = n_bullets

    def generate_bullet(self, shoot_position, facing_vector):
        # Generate 3 bullets, each one with 7.5 degrees of separation
        bullets = []
        half_spread = self.spread / 2

        spread_step = self.spread / self.n_bullets
        facingy, facingx = facing_vector
        facing_vector_angle = math.atan2(-facingy, facingx)
        initial_angle = facing_vector_angle - half_spread
        for i in range(0, self.n_bullets):
            # rotate facing vector i*15 degrees
            vector_angle = initial_angle + i * spread_step
            new_facingy = -math.sin(vector_angle)
            new_facingx = math.cos(vector_angle)
            new_facing_vector = np.array([new_facingy, new_facingx])
            bullets.append(super().generate_bullet(shoot_position, new_facing_vector))
        return bullets
