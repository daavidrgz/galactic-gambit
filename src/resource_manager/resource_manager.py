import pygame
import os

IMAGES_PATH = "assets/sprites"
SOUNDS_PATH = "assets/sounds"
COORDINATES_PATH = "coordenadas"

class ResourceManager(object):
    resources = {}

    @classmethod
    def loadImage(cls, name):
        if name in cls.resources:
           return cls.resources[name]
        else:
           fullname = os.path.join(IMAGES_PATH, name)
           image = pygame.image.load(fullname)
           cls.resources[name] = image
           return image

    @classmethod
    def loadSound(cls, name):
        if name in cls.resources:
           return cls.resources[name]
        else:
           fullname = os.path.join(SOUNDS_PATH, name)
           sound = pygame.mixer.Sound(fullname)
           cls.resources[name] = sound
           return sound
        


    @classmethod
    def loadCoordinatesFile(cls, name):
        if name in cls.resources:
           return cls.resources[name]
        else:
           fullname = os.path.join(COORDINATES_PATH, name)
           pfile = open(fullname, 'r')
           datos = pfile.read()
           pfile.close()
           cls.resources[name] = datos
           return datos
