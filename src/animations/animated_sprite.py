from animations.animation_frame import AnimationFrame
from systems.resource_manager import ResourceManager, Resource

import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, initial_pos):
        self.resource_manager = ResourceManager()
        self.speed_multiplier = 1.0

        if isinstance(frames, Resource):
            frames = self.resource_manager.load_animation(frames)
            self.current_anim = frames
        elif not isinstance(frames, list):
            frames = [AnimationFrame(frames, 0.1)]

        super().__init__()
        self.x, self.y = initial_pos
        self.setup_frames(frames)

    def on_animation_finished(self):
        pass

    def __binary_search_time(self, time):
        left = 0
        right = self.num_frames - 1
        while left <= right:
            mid = (left + right) // 2

            if self.acc_times[mid] <= time:
                left = mid + 1
            else:
                right = mid - 1
        # first item of the acc_times is 0, so left is always at least 1 at the end of the iteration
        return left - 1

    def update(self, elapsed_time):
        self.total_elapsed_time += elapsed_time * self.speed_multiplier
        if self.total_elapsed_time >= self.acc_times[-1]:
            self.on_animation_finished()

        self.total_elapsed_time %= self.acc_times[-1]
        next_frame_idx = self.__binary_search_time(self.total_elapsed_time)
        self.current_frame = self.frames[next_frame_idx]
        self.image = self.current_frame.get_image()

    def setup_frames(self, frames):
        self.frames = frames
        self.num_frames = len(frames)

        self.current_frame_idx = 0
        self.current_frame = self.frames[0]
        self.image = self.current_frame.get_image()
        self.image_rect = self.image.get_rect()
        self.rect = self.image_rect
        self.rect.center = (self.x, self.y)
        self.total_elapsed_time = 0

        self.acc_times = [0]
        for frame in self.frames:
            self.acc_times.append(self.acc_times[-1] + frame.get_duration())

    def set_animation(self, identifier):
        if identifier == self.current_anim:
            return
        self.current_anim = identifier
        frames = self.resource_manager.load_animation(identifier)
        self.setup_frames(frames)

    def set_speed_multiplier(self, value):
        self.speed_multiplier = value
