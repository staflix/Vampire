import pygame
import sys
from os import walk
from csv import reader

# базовые настройки игры
WIDTH, HEIGHT = SCREEN_SIZE = 1280, 720
TILE_SIZE = 32
FPS = 60

# информация о оружиях
type_of_attacks = {"lightning": {"cooldown": 2000, "damage": 30, "graphic": "graphics/lightning/lightning.png"},
                   "whip": {"cooldown": 1200, "damage": 15, "graphic": ""}}

# ui
bar_health = 20
health_bar_width = 200
border_money_height = 20
border_money_width = 100
border_health_height = 5
border_health_width = 32
size_font_number_of_money = 30
size_font_number_of_damage = 15
size_font_number_of_exp = 22

# ui colors
color_number_money = (0, 0, 0)
color_number_damage = (255, 0, 0)
color_border_money = (255, 255, 255)
color_border_health = (255, 0, 0)
color_border = (0, 0, 0)
color_border_exp = (55, 220, 255)
color_text = (0, 0, 0)


def import_csv_file(path):
    with open(path) as level_map:
        terrain_map = []
        data = reader(level_map, delimiter=',')
        for row in data:
            terrain_map.append(row)
        return terrain_map


def import_folder(path):
    surface_dict = {}
    for _, __, img_files in walk(path):
        img_files = sorted(img_files,
                           key=lambda x: int(x.split(".")[0]))
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            number = image.split(".")[0]
            surface_dict[str(number)] = image_surf
    return surface_dict


def disconnect():
    pygame.quit()
    sys.exit()
