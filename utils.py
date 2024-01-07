import pygame
import sys
from os import walk
from csv import reader

WIDTH, HEIGHT = SCREEN_SIZE = 1280, 720
TILE_SIZE = 32
FPS = 60


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
