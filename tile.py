import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        original_image = pygame.image.load("rock.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
