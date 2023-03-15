from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
from animations.explosion_effect import ExplosionEffect


class EnemyStrike(Projectile):
    def __init__(self, initial_pos, direction):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)
        self.timer = 200

        super().__init__(image, initial_pos, 5, direction, 0, 10)

    def collide(self, add_animation_func):
        pass

    def update(self, elapsed_time):
        super().update(elapsed_time)

        # Melee strikes last a fixed amount of time
        self.timer -= elapsed_time
        if self.timer <= 0:
            self.kill()

        # Player collision
        if self.rect.colliderect(self.level.player.rect):
            self.level.player.hit(self.damage, self.direction * self.knockback)
