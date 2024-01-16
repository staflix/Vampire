import pygame
import sys
from os import walk
from csv import reader
import time

# базовые настройки игры
WIDTH, HEIGHT = SCREEN_SIZE = 1280, 720
TILE_SIZE = 32
FPS = 60

# информация о оружиях
type_of_attacks = {"fireball": {"cooldown": 1000, "damage": 15},
                   "knife": {"cooldown": 2000, "damage": 15}}

# информация о врагах
enemies = {"bat": {"health": 10, "collide_damage": 1.5, "speed": 1.5},
           "spider": {"health": 15, "collide_damage": 4, "speed": 1.7},
           "squid": {"health": 20, "collide_damage": 8, "speed": 1.3}}

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
size_font_timer = 30

# ui colors
color_number_money = (0, 0, 0)
color_number_damage = (255, 0, 0)
color_border_money = (255, 255, 255)
color_border_health = (255, 0, 0)
color_border = (0, 0, 0)
color_border_exp = (55, 220, 255)
color_timer = (255, 255, 255)
color_exp = (255, 255, 255)

map_for_enemies = []


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
        img_files = sorted(img_files)
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            number = image.split(".")[0]
            surface_dict[str(number)] = image_surf
    return surface_dict


def get_elapsed_time(start_time):
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time


def disconnect():
    pygame.quit()
    sys.exit()
