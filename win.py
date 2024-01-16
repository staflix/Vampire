import pygame


class Win:
    def __init__(self, mobs_death):
        self.mobs_death = mobs_death
        self.display_surface = pygame.display.get_surface()
        self.width, self.height = self.display_surface.get_width(), self.display_surface.get_height()
        self.display_victory_message()

    def display_victory_message(self):
        font = pygame.font.Font(None, 36)
        text1 = font.render("Победа!!!", True, (255, 255, 255))
        text2 = font.render(f'Убито монстров: {self.mobs_death}', True, (255, 255, 255))

        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(text1, (self.width // 2 - text1.get_width() // 2, 200))
        self.display_surface.blit(text2, (self.width // 2 - text2.get_width() // 2, 300))

        pygame.display.flip()
