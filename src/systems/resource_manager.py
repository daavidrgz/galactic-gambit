from utils.singleton import Singleton

import pygame
import os


class ResourceManager(metaclass=Singleton):
    def __init__(self):
        self.resources = {}

        self.BASE_PATH = "assets"

        # Images
        self.PLAYER = "sprites/player.png"
        self.COBBLESTONE = "sprites/cobblestone.png"
        self.DIRT = "sprites/dirt.png"

        # Sounds (I dont know which ones we will use)
        self.ALIEN_SOUND = ("sounds/alien-sound.mp3",0.2)

        # Coordinates (Will we use them?)

    def load_image(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            fullname = os.path.join(self.BASE_PATH, name)
            try:
                image = pygame.image.load(fullname)
            except (pygame.error):
                print("Error loading image: ", fullname)
                raise SystemExit
            self.resources[name] = image
            return image

    def load_sound(self, sound):
        if sound[0] in self.resources:
            return self.resources[sound[0]]
        else:
            fullname = os.path.join(self.BASE_PATH, sound[0])
            try:
                loaded_sound = pygame.mixer.Sound(fullname)
            except (pygame.error):
                print("Error loading sound: ", fullname)
                raise SystemExit
            self.resources[sound[0]] = loaded_sound
            return loaded_sound

    def load_coordinates_file(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            fullname = os.path.join(self.BASE_PATH, name)
            try:
                pfile = open(fullname, "r")
                data = pfile.read()
                pfile.close()
            except (pygame.error):
                print("Error loading coord file: ", fullname)
                raise SystemExit
            self.resources[name] = data
            return data
