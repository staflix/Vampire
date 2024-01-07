from utils import *
from menu import Menu
from level import Level
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Vampire')
        self.screen = pygame.display.set_mode(SCREEN_SIZE, )
        self.level = Level()
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    disconnect()
            self.screen.fill("white")
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    menu = Menu(game.screen)
    mode = menu.run()
    if mode == "НАЧАТЬ":
        game.run()
    if mode == "УСИЛЕНИЯ":
        pass
