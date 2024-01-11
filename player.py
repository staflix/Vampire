from utils import *
import time
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, negative_sprites):
        super().__init__(groups)
        # player
        self.image = pygame.image.load("graphics/player/306.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.hitbox = self.rect.inflate(-10, -10)
        self.obstacle_sprites = obstacle_sprites
        self.negative_sprites = negative_sprites

        # animations
        self.animations = None
        self.type_walk = "down"

        # attacks
        self.last_lightning_time = pygame.time.get_ticks()
        self.last_knife_time = pygame.time.get_ticks()
        self.thunder = False
        self.knife = False

        # stats
        self.stats = {"hp": 100, "speed": 2, "exp_level": 1, "money": 0, "exp_to_level_up": 10}
        self.health = self.stats["hp"]
        self.speed = self.stats["speed"]
        self.exp_level = self.stats["exp_level"]
        self.money = self.stats["money"]
        self.exp_current_to_level_up = 8

        self.start_time = time.time()
        self.elapsed_time = 0

        self.load_images()

    def load_images(self):
        path = "graphics/player"
        self.animations = {
            "up": pygame.image.load(path + "/304.png").convert_alpha(),
            "right": pygame.image.load(path + "/305.png").convert_alpha(),
            "down": pygame.image.load(path + "/306.png").convert_alpha(),
            "left": pygame.image.load(path + "/307.png").convert_alpha()
        }

    def change_image_walk(self):
        self.image = self.animations[self.type_walk]

    def change_direction(self):
        # изменение направления вектора
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.type_walk = "up"
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.type_walk = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.type_walk = "right"
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.type_walk = "left"
        else:
            self.direction.x = 0

        if not keys:
            self.type_walk = "down"

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # moving top
                        self.hitbox.top = sprite.hitbox.bottom

        for sprite in self.negative_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.health -= 2

    def cooldown_thunder(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_lightning_time >= type_of_attacks["lightning"]["cooldown"]:
            self.thunder = True
            self.last_lightning_time = current_time

    def cooldown_knife(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_knife_time >= type_of_attacks["whip"]["cooldown"]:
            self.knife = True
            self.last_knife_time = current_time

    def level_up(self):
        pass

    def change_upgrade_and_info(self):
        pass

    def update(self):
        self.cooldown_thunder()
        self.cooldown_knife()
        self.change_direction()
        self.change_image_walk()
        self.move(self.speed)
