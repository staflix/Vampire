from utils import *
from tile import Tile
from player import Player
import pygame


class Level:
    def __init__(self):
        # создание видимых и препятственных спрайтов
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        # получение поверхности
        self.display_surface = pygame.display.get_surface()
        # отрисовка карты
        self.create_map()

    def create_map(self):
        for index_r, r in enumerate(world):
            for index_c, c in enumerate(r):
                x = index_c * TILE_SIZE
                y = index_r * TILE_SIZE
                if c == "!":
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                elif c == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        # обновение
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
