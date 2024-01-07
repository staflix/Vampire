from tile import Tile
from player import Player
from utils import *
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
        layouts = {
            "ground": import_csv_file("graphics/csvfiles/pygame_ground.csv"),
            "road": import_csv_file("graphics/csvfiles/pygame_road.csv"),
            "obstacles": import_csv_file("graphics/csvfiles/pygame_obstacles.csv")
        }
        pictures = {
            "ground": import_folder("graphics/ground"),
            "road": import_folder("graphics/road"),
            "obstacles": import_folder("graphics/obstacles"),
        }

        for style, layout in layouts.items():
            for index_r, r in enumerate(layout):
                for index_c, c in enumerate(r):
                    if c != "-1":
                        x = index_c * TILE_SIZE
                        y = index_r * TILE_SIZE
                        if style == "obstacles":
                            obj = pictures["obstacles"][str(c)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], "obstacles", obj)

        self.player = Player((1500, 1600), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        # обновение
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.player.update()
        if self.player.thunder:
            print("Thunder!")
            self.player.thunder = False
        if self.player.knife:
            print("Knife!")
            self.player.knife = False


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # отрисовка фона
        self.floor_surf = pygame.image.load("graphics/fon.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # рисование фона
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        # рисование всех спрайтов по центру относительно игрока
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
