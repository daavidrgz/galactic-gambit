from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
from animations.explosion_effect import ExplosionEffect


class EnemyStrike(Projectile):
    def __init__(self, initial_pos, direction):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)

        super().__init__(image, initial_pos, 5, direction, 0, 10, 200)
        self.ground_collision = False

    def update(self, elapsed_time):
        super().update(elapsed_time)

        # Player collision
        if self.rect.colliderect(self.level.player.rect):
            self.level.player.hit(self.damage, self.get_direction() * self.knockback)
