import pygame as pg
from utils.singleton import Singleton
from systems.resource_manager import ResourceManager
import os

class SoundController(metaclass=Singleton):
    music_volume = 100
    effects_volume = 100
    relative_volume = 1

    @classmethod
    def __init__(self):
        self.resource_manager = ResourceManager.get_instance()
        pg.mixer.pre_init(44100,-16,2, 512) # Default values used by PyGame
        pg.mixer.init()

    @classmethod
    def play():
        pg.mixer.music.unpause()
    
    @classmethod
    def pause():
        pg.mixer.music.pause()

    @classmethod
    def update_music_volume(self, volume):
        self.music_volume = volume
        self.set_relative_volume_music()
        
    @classmethod
    def update_effects_volume(self, volume):
        self.effects_volume = volume

    @classmethod
    def get_music_volume(self):
        return self.music_volume
    
    @classmethod
    def get_effects_volume(self):
        return self.effects_volume

    @classmethod
    def set_relative_volume_music(self, rel_volume = -1):
        if rel_volume != -1:                        # This is done to maintain the relative volume when changing the music volume
            self.relative_volume = rel_volume
        pg.mixer.music.set_volume(self.relative_volume * self.music_volume/100)

    @classmethod
    def set_relative_volume_sound(self, loaded_sound, rel_volume = 1):
        loaded_sound.set_volume(rel_volume * self.effects_volume/100)

    @classmethod
    def play_music(self, music):
        pg.mixer.music.load(os.path.join(self.resource_manager.BASE_PATH, music[0]))
        self.set_relative_volume_music(music[1])
        pg.mixer.music.play(-1)

    @classmethod
    def play_sound(self, sound):
        loaded_sound = self.resource_manager.load_sound(sound)
        self.set_relative_volume_sound(loaded_sound, sound[1])
        loaded_sound.play()
    