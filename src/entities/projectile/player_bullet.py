from animations.explosion_effect import ExplosionEffect
from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
from utils.math import circle_rect_collision


class PlayerBullet(Projectile):
    def __init__(
        self,
        initial_pos,
        speed,
        direction,
        damage,
        knockback,
        lifetime,
        upgrades,
    ):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.PLAYER_PROJECTILE)
        self.upgrades = upgrades
        self.size = 4
        super().__init__(
            image, initial_pos, speed, direction, damage, knockback, lifetime
        )

    def collide(self, add_animation_func):
        add_animation_func(ExplosionEffect(self.position))
        super().collide(add_animation_func)

    def setup(self, level):
        super().setup(level)
        [u.init_effect(self, level) for u in self.upgrades if u.init_effect is not None]

    def update(self, elapsed_time):
        super().update(elapsed_time)
        [
            u.update_effect(self, elapsed_time)
            for u in self.upgrades
            if u.update_effect is not None
        ]

        # Enemy collision
        for enemy in self.level.enemy_group:
            if circle_rect_collision(
                (self.position[0], self.position[1], self.size), enemy.rect
            ):
                enemy.hit(self.damage, self.get_direction() * self.knockback)
                self.kill()
                break
