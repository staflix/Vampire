from utils import *
import time
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, negative_sprites):
        # Вызов конструктора родительского класса
        super().__init__(groups)

        # Инициализация параметров игрока
        self.image = pygame.image.load("graphics/player/306.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.hitbox = self.rect.inflate(-10, -10)
        self.obstacle_sprites = obstacle_sprites
        self.negative_sprites = negative_sprites

        # Анимации игрока
        self.animations = None
        self.type_walk = "down"

        # Атаки игрока
        self.last_knife_time = pygame.time.get_ticks()
        self.knife = False

        # Статистика игрока
        self.stats = {"hp": 100, "speed": 2, "exp_level": 1, "exp_to_level_up": 10}
        self.health = self.stats["hp"]
        self.speed = self.stats["speed"]
        self.exp_level = self.stats["exp_level"]
        self.next_level = self.stats["exp_to_level_up"]
        self.exp_current_to_level_up = 0

        # Время
        self.start_time = time.time()
        self.elapsed_time = 0

        # Загрузка анимаций
        self.load_images()

        # Статистика убитых мобов
        self.mobs_death = 0

    def load_images(self):
        # Загрузка изображений анимаций для разных направлений движения
        path = "graphics/player"
        self.animations = {
            "up": pygame.image.load(path + "/304.png").convert_alpha(),
            "right": pygame.image.load(path + "/305.png").convert_alpha(),
            "down": pygame.image.load(path + "/306.png").convert_alpha(),
            "left": pygame.image.load(path + "/307.png").convert_alpha()
        }

    def change_image_walk(self):
        # Смена изображения при ходьбе в разных направлениях
        self.image = self.animations[self.type_walk]

    def change_direction(self):
        # Изменение направления движения в соответствии с нажатыми клавишами
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
        # Движение игрока
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        # Обработка столкновений игрока с препятствиями и врагами
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Движение вправо
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Движение влево
                        self.hitbox.left = sprite.hitbox.right
        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Движение вниз
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Движение вверх
                        self.hitbox.top = sprite.hitbox.bottom

            for sprite in self.negative_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.health -= 0.1

    def death(self):
        # Обработка смерти игрока
        if self.health <= 0:
            disconnect()

    def cooldown_knife(self):
        # Обработка времени восстановления для атаки ножом
        current_time = pygame.time.get_ticks()
        if current_time - self.last_knife_time >= type_of_attacks["knife"]["cooldown"]:
            self.knife = True
            self.last_knife_time = current_time

    def update_level(self):
        # Обновление уровня игрока при убийстве врага
        self.exp_current_to_level_up += 1
        if self.exp_current_to_level_up >= self.next_level:
            self.exp_level += 1
            self.exp_current_to_level_up = 0

    def update(self):
        # Обновление параметров игрока в каждом кадре
        self.cooldown_knife()
        self.change_direction()
        self.change_image_walk()
        self.death()
        self.move(self.speed)
