import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/zastavka.jpg").convert()
        self.rect = self.image.get_rect()
