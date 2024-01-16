from utils import *
import time
from win import Win
import pygame


class UI:
    def __init__(self, offset):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = offset
        self.start_time = time.time()

    def visual(self, player):
        # визуализация здоровья персонажа
        health_bar_rect = pygame.Rect(player.rect.x - self.offset.x, player.rect.y - self.offset.y + 32,
                                      border_health_width, border_health_height)
        background_health_rect = health_bar_rect.copy()

        # вижуализация уровня персонажа
        exp_bar_rect = pygame.Rect(440, 10, 420, 14)
        background_exp_bar_rect = exp_bar_rect.copy()

        # сколько хп и экспы в одном пикселе
        ratio_health = player.health / player.stats["hp"]
        ratio_exp = player.exp_current_to_level_up / player.stats["exp_to_level_up"]

        # изменение длины баров
        current_width_exp = exp_bar_rect.width * ratio_exp
        current_rect_exp = exp_bar_rect.copy()
        current_rect_exp.width = current_width_exp

        current_width_health = health_bar_rect.width * ratio_health
        current_rect_health = health_bar_rect.copy()
        current_rect_health.width = current_width_health

        # отрисовка
        self.update(current_rect_health, background_health_rect, background_exp_bar_rect, current_rect_exp, player)

    def format_time(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update(self, health_rect, background_health, background_exp_rect, exp_rect, player):
        # отрисовка здоровья
        pygame.draw.rect(self.display_surface, color_border, background_health)
        pygame.draw.rect(self.display_surface, color_border_health, health_rect)

        # отрисовка уровня
        pygame.draw.rect(self.display_surface, color_border, background_exp_rect)
        pygame.draw.rect(self.display_surface, color_border_exp, exp_rect)

        # размер шрифта для уровня
        font_exp = pygame.font.Font(None, size_font_number_of_exp)

        # отображение уровня
        exp_text = font_exp.render(str(player.exp_level), True, color_exp)
        self.display_surface.blit(exp_text, (background_exp_rect.x + 2, background_exp_rect.y + 1))

        # время в игре
        elapsed_time = get_elapsed_time(self.start_time)
        formatted_time = self.format_time(elapsed_time)

        font_timer = pygame.font.Font(None, size_font_timer)
        timer_text = font_timer.render(formatted_time, True, color_timer)
        self.display_surface.blit(timer_text, (10, 10))
        # Проверка времени и отключение, если прошло 10 минут
        if elapsed_time > 10:
            player.win_lose = True
            Win(player.mobs_death)
        elif elapsed_time > 20:
            disconnect()
