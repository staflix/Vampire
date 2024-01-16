from tile import Tile
from player import Player
from utils import *
from ui import UI
from enemy import Enemy
from knife import Knife
import random
import time
import pygame


class Level:
    def __init__(self):
        # создание видимых, препятственных, злых спрайтов
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.negative_sprites = pygame.sprite.Group()
        self.count = 1
        # получение поверхности
        self.display_surface = pygame.display.get_surface()
        # объекты
        self.layouts = {
            "obstacles": import_csv_file("graphics/csvfiles/pygame_obstacles.csv")
        }
        self.pictures = {
            "obstacles": import_folder("graphics/obstacles"),
        }
        # отрисовка карты
        self.create_map()
        # начало отсчета времени
        self.start_time = time.time()
        self.elapsed_time = 0
        self.old_elapsed_time = -8

    def create_map(self):
        for style, layout in self.layouts.items():
            for index_r, r in enumerate(layout):
                for index_c, c in enumerate(r):
                    x = index_c * TILE_SIZE
                    y = index_r * TILE_SIZE
                    if c != "-1":
                        if style == "obstacles":
                            obj = self.pictures["obstacles"][str(c)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], obj)
        self.player = Player((1500, 1600), [self.visible_sprites], self.obstacles_sprites, self.negative_sprites)

    def update_monsters(self, count_monsters, type_monsters):
        correct_position = []

        for style, layout in self.layouts.items():
            for index_r, r in enumerate(layout):
                for index_c, c in enumerate(r):
                    if c == "-1" and 19 < index_r < 80 and 19 < index_c < 80:
                        x = index_c * TILE_SIZE
                        y = index_r * TILE_SIZE
                        correct_position.append((x, y))

        for i in range(count_monsters):
            if correct_position:
                chosen_position = random.choice(correct_position)
                x = chosen_position[0]
                y = chosen_position[1]
                Enemy(self.player, type_monsters, (x, y), [self.visible_sprites, self.negative_sprites],
                      self.obstacles_sprites, self.negative_sprites)

    def run(self):
        # обновение
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.elapsed_time = get_elapsed_time(self.start_time)
        if self.elapsed_time - self.old_elapsed_time >= 10:
            self.old_elapsed_time = self.elapsed_time
            if self.elapsed_time < 60:
                self.update_monsters(10, "squid")
            elif self.elapsed_time < 120:
                self.update_monsters(12, "bat")
            elif self.elapsed_time < 180:
                self.update_monsters(15, "spider")
            elif self.elapsed_time < 240:
                self.update_monsters(19, "squid")
            elif self.elapsed_time < 300:
                self.update_monsters(22, "spider")
            elif self.elapsed_time < 360:
                self.update_monsters(15, "spider")
            elif self.elapsed_time < 420:
                self.update_monsters(17, "squid")
            elif self.elapsed_time < 480:
                self.update_monsters(19, "bat")
            elif self.elapsed_time < 540:
                self.update_monsters(20, "squid")
        if self.player.knife:
            Knife(self.player, [self.visible_sprites], "knife", self.negative_sprites, self.player.exp_level)

        self.player.update()


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

        self.ui = UI(self.offset)

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # рисование фона
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # рисование всех спрайтов кроме игрока
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            if sprite != player:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # рисование игрока
        offset_pos = player.rect.topleft - self.offset
        self.display_surface.blit(player.image, offset_pos)

        self.ui.visual(player)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type")
                         and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
