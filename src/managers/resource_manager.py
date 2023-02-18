import pygame
import os


class ResourceManager(object):
    __instance = None
    resources = {}

    BASE_PATH = "assets"

    # Images
    PLAYER = "sprites/player.png"

    # Sounds (I dont know which ones we will use)

    # Coordinates (Will we use them?)

    def get_instance():
        if ResourceManager.__instance is None:
            ResourceManager.__instance = ResourceManager()
        return ResourceManager.__instance

    @classmethod
    def loadImage(self, name):
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

    @classmethod
    def loadSound(self, name):
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

    @classmethod
    def loadCoordinatesFile(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            fullname = os.path.join(self.BASE_PATH, name)
            try:
                pfile = open(fullname, "r")
                datos = pfile.read()
                pfile.close()
            except (pygame.error):
                print("Error loading coord file: ", fullname)
                raise SystemExit
            self.resources[name] = datos
            return datos
