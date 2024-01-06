import pygame
import sys

WIDTH, HEIGHT = SCREEN_SIZE = 1280, 720
TILE_SIZE = 32
FPS = 60

world = []
with open("map1.txt", "r", encoding="utf-8") as map_file:
    data = map_file.readlines()
    for row in data:
        world.append(row.strip())


def disconnect():
    pygame.quit()
    sys.exit()
