from utils import *
import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = {"НАЧАТЬ": ((540, 500, 200, 45), (3, 102, 173), (0, 149, 255)),
                        "ВЫЙТИ": ((540, 550, 200, 45), (180, 0, 0), (255, 0, 0)),
                        "УСИЛЕНИЯ": ((540, 600, 200, 45), (3, 102, 173), (0, 149, 255))}
        self.clock = pygame.time.Clock()
        self.sprite_buttons = pygame.sprite.Group()

    def run(self):
        flag_click = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    disconnect()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    flag_click = True
                if flag_click and event.type == pygame.MOUSEBUTTONUP:
                    name_click_btn = self.click_check(event.pos)
                    if name_click_btn == "ОТМЕНА":
                        disconnect()
                    return name_click_btn
            self.screen.fill('black')
            self.create_buttons()
            self.sprite_buttons.update()
            self.sprite_buttons.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def create_buttons(self):
        self.sprite_buttons.empty()
        for text, info in self.buttons.items():
            button = Button(text, info[0], info[1], info[2])
            button.add(self.sprite_buttons)

    def click_check(self, pos):
        for button in self.sprite_buttons:
            if isinstance(button, Button) and button.rect.collidepoint(pos):
                return button.name


class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, hover_color):
        super().__init__()
        self.font = pygame.font.SysFont("", 36)
        self.name = text
        self.text_image = self.font.render(text, True, (255, 255, 255))
        self.width = pos[2]
        self.height = pos[3]
        self.color = color
        self.hover_color = hover_color
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos[:2])
        self.rect.topleft = pos[:2]
        self.is_hovered = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.draw()

    def draw(self):
        if self.is_hovered:
            pygame.draw.rect(self.image, self.hover_color, (0, 0, self.width, self.height), border_radius=10)
        else:
            pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), border_radius=10)
        text_rect = self.text_image.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(self.text_image, text_rect)
