from utils import *
import pygame


class Knife(pygame.sprite.Sprite):
    def __init__(self, player, groups, weapon_name, negative_sprites, exp_level):
        super().__init__(groups)
        self.player = player
        self.weapon_name = weapon_name
        self.frame_index = 1  # Start with frame 0
        self.negative_sprites = negative_sprites
        self.image = pygame.image.load("graphics/knife/1.png")
        self.rect = self.image.get_rect(midleft=player.rect.midright)
        self.damage = type_of_attacks["knife"]["damage"] + exp_level * 2
        self.start_time = time.time()

    def animate(self):
        if time.time() - self.start_time >= 0.1:
            self.player.knife = False

    def collision(self):
        for sprite in self.negative_sprites:
            if self.rect.colliderect(sprite.rect):
                sprite.receive_damage_knife(self.damage)

    def update(self):
        if self.player.knife:
            self.rect = self.image.get_rect(midleft=self.player.rect.midright)
            self.animate()
            self.collision()
        else:
            self.kill()
