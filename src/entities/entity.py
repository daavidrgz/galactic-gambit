from animations.animated_sprite import AnimatedSprite
from animations.animation_frame import AnimationFrame


class Entity(AnimatedSprite):
    def __init__(self, frames, hitbox, initial_pos):
        if not isinstance(frames, list):
            frames = [AnimationFrame(frames, 0.1)]
        super().__init__(frames, initial_pos)

        self.rect = hitbox
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def setup(self):
        pass

    def update(self, elapsed_time):
        super().update(elapsed_time)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position
        self.rect.centerx, self.rect.centery = self.x, self.y

    def move(self, delta_position):
        deltax, deltay = delta_position
        currentx, currenty = self.get_position()
        self.set_position((currentx + deltax, currenty + deltay))
