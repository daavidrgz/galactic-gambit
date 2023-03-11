import pygame
from entities.kinematic_entity import KinematicEntity


class LivingEntity(KinematicEntity):
    HIT_DURATION = 250

    def __init__(self, image, initial_pos, drag, collision, hp):
        super().__init__(image, initial_pos, drag, collision)
        self.hp = hp
        self.was_hit = False
        self.hit_timer = 0

    def update(self, elapsed_time):
        self.__check_alive()
        if self.was_hit:
            self.hit_timer -= elapsed_time
            if self.hit_timer <= 0:
                self.was_hit = False
                self.remove_image_modifier(self.__hit_sprite_modifier)
        super().update(elapsed_time)

    def hit(self, damage):
        if self.was_hit:
            return
        self.was_hit = True
        self.hit_timer = self.HIT_DURATION
        self.hp = max(0.0, self.hp - damage)
        self.add_image_modifier(self.__hit_sprite_modifier)

    def __hit_sprite_modifier(self, image):
        color = (255, 0, 0)
        veil = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        veil.fill(color)
        veil.set_alpha(128)
        image.blit(veil, (0, 0))

    def is_alive(self):
        return self.hp > 0.0

    def __check_alive(self):
        if not self.is_alive():
            self.kill()
