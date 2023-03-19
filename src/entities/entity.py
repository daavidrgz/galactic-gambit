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

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def move(self, delta_position):
        deltax, deltay = delta_position
        currentx, currenty = self.get_position()
        self.set_position((currentx + deltax, currenty + deltay))

    def collide(self, on_colide):
        pass

    def kill(self):
        self.removed = True
        super().kill()

    def get_id(self):
        return self.id
