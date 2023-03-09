import pygame as pg
from utils.singleton import Singleton
from systems.resource_manager import Resource, ResourceManager
import os


class SoundController(metaclass=Singleton):
    music_volume = 100
    effects_volume = 100
    relative_volume = 1
    volume_step = 1

    def __init__(self):
        self.resource_manager = ResourceManager()
        pg.mixer.pre_init(44100, -16, 2, 512)  # Default values used by PyGame
        pg.mixer.init()

    def play(self):
        pg.mixer.music.unpause()

    def pause(self):
        pg.mixer.music.pause()

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
        pg.mixer.music.load(
            os.path.join(self.resource_manager.BASE_PATH, music.value[0])
        )
        self.set_relative_volume_music(music.value[1])
        pg.mixer.music.play(-1)

    def play_sound(self, sound):
        loaded_sound = self.resource_manager.load_sound(sound)
        self.set_relative_volume_sound(loaded_sound, sound.value[1])
        loaded_sound.play()
