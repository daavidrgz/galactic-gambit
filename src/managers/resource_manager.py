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

    def load_sound(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            fullname = os.path.join(self.BASE_PATH, name)
            try:
                sound = pygame.mixer.Sound(fullname)
            except (pygame.error):
                print("Error loading sound: ", fullname)
                raise SystemExit
            self.resources[name] = sound
            return sound

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
