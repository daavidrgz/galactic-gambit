import pygame

class Terrain():
    def __init__(self, sprites, generation_mask, starting_tile):
        self.sprites = sprites
        self.generation_mask = generation_mask
        self.starting_tile = starting_tile
        self.height, self.width = generation_mask.shape

    def draw(self, screen):
        self.sprites.draw(screen)

    #TODO
