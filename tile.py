import pygame
from utils import TILE_SIZE


# объект
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
