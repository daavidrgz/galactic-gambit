from entities.kinematic_entity import KinematicEntity
from entities.living.hp import Hp
from utils.observable import Observable

import pygame

from constants.game_constants import HIT_INVULNERABILITY_TIME


class ObservablePosition(Observable):
    def __init__(self, entity_id):
        self.entity_id = entity_id
        super().__init__()

    def update(self, position):
        self.notify_listeners(self.entity_id, position)


class LivingEntity(KinematicEntity):
    def __init__(self, image, initial_pos, drag, collision, hp):
        super().__init__(image, initial_pos, drag, collision)
        self.hp = Hp(hp)
        self.was_hit = False
        self.hit_timer = 0
        self.observable_pos = ObservablePosition(self.id)

    def update(self, elapsed_time):
        if self.was_hit:
            self.hit_timer -= elapsed_time
            if self.hit_timer <= 0:
                self.was_hit = False
                self.remove_image_modifier(self.__hit_sprite_modifier)

        super().update(elapsed_time)

        self.observable_pos.update((self.x, self.y))

    def setup(self):
        self.hp.setup(self)
        super().setup()

    def hit(self, damage, knockback=None):
        if self.was_hit:
            return
        self.was_hit = True
        self.hit_timer = HIT_INVULNERABILITY_TIME
        self.hp.reduce(damage)
        self.add_image_modifier(self.__hit_sprite_modifier)

        if knockback is not None:
            self.velocity += knockback

    def __hit_sprite_modifier(self, image):
        color = 255, 37, 23
        hit_mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        hit_mask.fill(color)
        hit_mask.set_alpha(255 * (self.hit_timer / HIT_INVULNERABILITY_TIME))
        image.blit(hit_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def on_death(self):
        self.observable_pos.update(None)
