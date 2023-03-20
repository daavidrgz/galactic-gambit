from animations.animated_sprite import AnimatedSprite


class Entity(AnimatedSprite):
    ID_COUNT = 0

    def __init__(self, image, initial_pos):
        super().__init__(image, initial_pos)

        self.id = Entity.ID_COUNT
        Entity.ID_COUNT += 1

        self.removed = False

    def setup(self, level):
        self.level = level

    def update(self, elapsed_time):
        super().update(elapsed_time)

    def collide(self, on_colide):
        pass

    def kill(self):
        self.removed = True
        super().kill()

    def get_id(self):
        return self.id
