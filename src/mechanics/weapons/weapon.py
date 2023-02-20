from entities.projectile.bullet import Bullet


class Weapon:
    def __init__(self, damage, cooldown, bullet_speed, gun_offset):
        self.damage = damage
        self.initial_cooldown = cooldown
        self.cooldown = 0.0
        self.bullet_speed = bullet_speed
        self.gun_offset = gun_offset

    def is_ready(self):
        return self.cooldown == 0.0

    def update_cooldown(self, elapsed_time):
        self.cooldown = max(0.0, self.cooldown - elapsed_time)

    def shoot(self, shoot_position, facing_vector):
        # Maybe we do not need to parameter gun_offset, but for snipers may be usefull to simulate
        # a barrel distance.
        self.cooldown = self.initial_cooldown
        return self.generate_bullet(shoot_position, facing_vector)

    def generate_bullet(self, shoot_position, facing_vector):
        initial_position = shoot_position + facing_vector * self.gun_offset
        return Bullet(initial_position, self.bullet_speed, facing_vector)
