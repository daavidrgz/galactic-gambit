from animations.animated_sprite import AnimatedSprite


class Effect(AnimatedSprite):
    def __init__(self, frames, initial_pos):
        super().__init__(frames, initial_pos)

    def on_animation_finished(self):
        self.kill()
