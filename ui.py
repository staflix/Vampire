from utils import *
import pygame


class UI:
    def __init__(self, offset):
        self.display_surface = pygame.display.get_surface()
        self.offset = offset

    def health_and_exp_bars(self, player):
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
        exp_text = font_exp.render(str(player.exp_level), True, color_text)
        self.display_surface.blit(exp_text, (background_exp_rect.x + 2, background_exp_rect.y + 1))



