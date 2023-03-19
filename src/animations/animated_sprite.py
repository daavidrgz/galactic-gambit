import copy

import numpy as np
from animations.animation_frame import AnimationFrame
from systems.resource_manager import ResourceManager, Resource

import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, initial_pos):
        self.resource_manager = ResourceManager.get_instance()
        self.speed_multiplier = 1.0
        self.x, self.y = initial_pos
        self.modifiers = []

        if isinstance(frames, Resource):
            frames = self.resource_manager.load_animation(frames)
            self.current_anim = frames
        elif not isinstance(frames, list):
            frames = [AnimationFrame(frames, 0.1)]

        self.current_frame_size = None
        self.setup_frames(frames)

        super().__init__()

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
        current_frame_image = self.current_frame.get_image()

        # Reset rect every frame, so modifications applied to the sprite does not affect the original rect
        self._rect = current_frame_image.get_rect()

        # Use a buffer image to blit current frame, and do not use self.image directly, because
        # other sources (e.g. upgrades) could modify self.image size. This way, we can keep the
        # original image size
        self.__buffer_image.fill((0, 0, 0, 0))
        self.__buffer_image.blit(current_frame_image, (0, 0))
        self.image = self.__buffer_image
        self.__apply_image_modifiers()

    def add_image_modifier(self, modifier):
        self.modifiers.append(modifier)

    def remove_image_modifier(self, modifier):
        self.modifiers.remove(modifier)

    def __apply_image_modifiers(self):
        for modifier in self.modifiers:
            modifier(self.image)

    def setup_frames(self, frames):
        # Use first frame size as image size. All frames must have the same image size
        frame_size = frames[0].get_image().get_size()
        if frame_size != self.current_frame_size:
            self.current_frame_size = frame_size
            self.__buffer_image = pygame.Surface(frame_size, pygame.SRCALPHA)

        self.frames = frames
        self.num_frames = len(frames)

        self.current_frame_idx = 0
        self.current_frame = self.frames[0]
        self.__buffer_image.blit(self.current_frame.get_image(), (0, 0))
        self.image = self.__buffer_image
        self._rect = self.__buffer_image.get_rect()
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

    def set_image(self, image):
        self.current_anim = None
        if not isinstance(image, list):
            image = [AnimationFrame(image, 0.1)]
        self.setup_frames(image)

    @property
    def rect(self):
        self._rect.centerx, self._rect.centery = self.x, self.y
        return self._rect
