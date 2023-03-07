class AnimationFrame:
    def __init__(self, image, duration):
        self.image = image
        self.duration = duration

    def get_image(self):
        return self.image

    def get_duration(self):
        return self.duration
