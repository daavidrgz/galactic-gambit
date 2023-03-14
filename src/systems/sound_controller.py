from itertools import cycle
import random
import pygame as pg
from utils.singleton import Singleton
from systems.resource_manager import ResourceManager
import os


class RandomSounds:
    def __init__(self, sound_resources, delay=0, volume_variation=0):
        self.sound_controller = SoundController.get_instance()
        self.resource_manager = ResourceManager.get_instance()
        self.sound_resources = sound_resources
        self.delay = delay
        self.current_delay = 0
        self.playing = False

    def update(self, elapsed_time):
        if not self.playing:
            return
        self.current_delay += elapsed_time
        if self.current_delay >= self.delay:
            self.sound_controller.play_sound(random.choice(self.sound_resources))
            self.current_delay = 0

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False


class CycleSounds:
    def __init__(self, sounds_resource, delay=0, volume_variation=0):
        self.sound_controller = SoundController.get_instance()
        self.resource_manager = ResourceManager.get_instance()
        loaded_sounds = self.resource_manager.load_sounds(sounds_resource)
        self.sounds = cycle(loaded_sounds)
        self.volume_variation = volume_variation
        self.playing = False
        self.delay = delay
        self.current_delay = 0

    def __play_sound(self, sound):
        volume = random.randint(0, int(self.volume_variation * 100)) / 100 + (
            sound[1] - self.volume_variation
        )
        self.sound_controller.play_sound_raw(sound[0], volume)

    def update(self, elapsed_time):
        if not self.playing:
            return
        self.current_delay += elapsed_time
        if self.current_delay >= self.delay:
            self.__play_sound(next(self.sounds))
            self.current_delay = 0

    def play_once(self):
        self.__play_sound(next(self.sounds))

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False


class SoundController(metaclass=Singleton):
    music_volume = 50
    effects_volume = 100
    relative_volume = 1
    volume_step = 1

    def __init__(self):
        self.resource_manager = ResourceManager()
        pg.mixer.pre_init(44100, -16, 2, 512)  # Default values used by PyGame
        pg.mixer.init()
        self.current_music = None

    def play(self):
        pg.mixer.music.unpause()

    def pause(self):
        pg.mixer.music.fadeout(1000)

    def set_music_volume(self, volume):
        self.music_volume = volume
        self.set_relative_volume_music()

    def set_effects_volume(self, volume):
        self.effects_volume = volume

    def get_music_volume(self):
        return self.music_volume

    def get_effects_volume(self):
        return self.effects_volume

    def increase_music_volume(self):
        self.music_volume = min(100, self.music_volume + self.volume_step)
        self.set_relative_volume_music()
        return self.music_volume

    def decrease_music_volume(self):
        self.music_volume = max(0, self.music_volume - self.volume_step)
        self.set_relative_volume_music()
        return self.music_volume

    def increase_effects_volume(self):
        self.effects_volume = min(100, self.effects_volume + self.volume_step)
        return self.effects_volume

    def decrease_effects_volume(self):
        self.effects_volume = max(0, self.effects_volume - self.volume_step)
        return self.effects_volume

    def set_relative_volume_music(self, rel_volume=-1):
        if (
            rel_volume != -1
        ):  # This is done to maintain the relative volume when changing the music volume
            self.relative_volume = rel_volume
        pg.mixer.music.set_volume(self.relative_volume * self.music_volume / 100)

    def set_relative_volume_sound(self, loaded_sound, rel_volume=1):
        loaded_sound.set_volume(rel_volume * self.effects_volume / 100)

    def play_music(self, music):
        if self.current_music == music:
            return
        if pg.mixer.music.get_busy():
            self.pause()
        pg.mixer.music.load(
            os.path.join(self.resource_manager.BASE_PATH, music.value[0])
        )
        self.set_relative_volume_music(music.value[1])
        pg.mixer.music.play(-1)
        self.current_music = music

    def play_sound(self, sound, max_time=0):
        loaded_sound = self.resource_manager.load_sound(sound)
        self.set_relative_volume_sound(loaded_sound, sound.value[1])
        loaded_sound.play(maxtime=max_time)

    def play_sound_raw(self, sound, volume):
        self.set_relative_volume_sound(sound, volume)
        sound.play()
