from entities.projectile.projectile import Projectile
from systems.resource_manager import ResourceManager


class EnemyStrike(Projectile):
    def __init__(
        self, attack_image, initial_pos, speed, direction, damage, knockback, lifetime
    ):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(attack_image)

        super().__init__(
            image, initial_pos, speed, direction, damage, knockback, lifetime
        )
        self.ground_collision = False

    def update(self, elapsed_time):
        super().update(elapsed_time)

        # Player collision
        if self.rect.colliderect(self.level.player.rect):
            self.level.player.hit(self.damage, self.get_direction() * self.knockback)
