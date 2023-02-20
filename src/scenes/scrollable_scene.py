import pygame
from entities.entity import Entity
from scenes.scene import Scene
from constants import DESIGN_WIDTH, DESIGN_HEIGHT


class ScrollableScene(Scene):
    def __init__(self):
        super().__init__()
        self.scroll = Scroll((0, 0))


class Scroll:
    __scroll_width = DESIGN_WIDTH
    __scroll_height = DESIGN_HEIGHT

    def __init__(self, initial_scroll):
        self.scrollx, self.scrolly = initial_scroll

    def get_scroll(self):
        return self.scrollx, self.scrolly

    def set_scroll(self, scroll):
        self.scrollx, self.scrolly = scroll

    def move_scroll(self, scroll):
        deltax, deltay = scroll
        self.scrollx += deltax
        self.scrolly += deltay

    def center_at(self, sprite):
        self.scrollx = sprite.x - self.__scroll_width // 2
        self.scrolly = sprite.y - self.__scroll_height // 2
        return self


class ScrollableGroup(pygame.sprite.Group):
    def __init__(self, scroll, *sprites):
        super().__init__(sprites)
        self.scroll = scroll

    def draw(self, surface):
        scrollx, scrolly = self.scroll.get_scroll()
        sprites = self.sprites()

        def calculate_rect(entity: Entity):
            copy = entity.image_rect.copy()
            copy.centerx = entity.x - scrollx
            copy.centery = entity.y - scrolly
            return copy

        if hasattr(surface, "blits"):

            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, calculate_rect(spr)) for spr in sprites),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, calculate_rect(spr))
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
