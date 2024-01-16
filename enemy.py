from utils import *
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, enemy_name, pos, groups, obstacle_sprites, negative_sprites):
        super().__init__(groups)
        self.player = player
        self.animations = self.import_graphics(enemy_name)
        self.sprite_type = "enemy"
        self.frame_index = 1
        self.animation_time = 0.15
        self.direction = pygame.math.Vector2()
        self.image = self.animations["move"][str(self.frame_index)]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        self.negative_sprites = negative_sprites
        self.monster_name = enemy_name
        self.health = enemies[self.monster_name]["health"]
        self.speed = enemies[self.monster_name]["speed"]
        self.collide_damage = enemies[self.monster_name]["collide_damage"]
        self.get_damage_knife = False
        self.last_damage_time_knife = 0
        self.last_fireball_damage_time = 0
        self.get_damage_fireball = False
        self.damage_sprite = pygame.sprite.Group()

    def import_graphics(self, name):
        animations = {"move": []}
        main_path = f'graphics/monsters/{name}/'
        for animation in animations.keys():
            animations[animation] = import_folder(main_path)
        return animations

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return direction

    def animate(self):
        animation = self.animations["move"]
        self.frame_index += self.animation_time
        if self.frame_index >= len(animation):
            self.frame_index = 1
        self.image = animation[str(int(self.frame_index))]
        self.rect = self.image.get_rect(center=self.hitbox.center)

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

    def receive_damage_knife(self, damage, cooldown=0.2):
        current_time = pygame.time.get_ticks()
        if not self.get_damage_knife and current_time >= self.last_damage_time_knife + cooldown * 1000:
            self.health -= damage
            if self.health > 0:
                self.image = pygame.image.load(f'graphics/monsters/{self.monster_name}/5.png').convert_alpha()
            else:
                self.death()
            self.get_damage_knife = True
            self.last_damage_time_knife = current_time

    def death(self):
        self.kill()
        self.player.update_level()
        self.player.mobs_death += 1

    def enemy_update(self, player):
        self.get_damage_knife = False
        self.get_damage_fireball = False
        self.direction = self.get_player_distance_direction(player)
        self.animate()
        self.move(self.speed)
