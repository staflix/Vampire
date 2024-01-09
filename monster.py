from utils import *
import pygame


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, groups, hp, speed, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.hp = hp
        self.speed = speed
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
