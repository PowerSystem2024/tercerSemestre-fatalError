import pygame
from core.game import Game
from screens.login import show_login

def main():
    pygame.init()
    screen = pygame.display.set_mode((1064, 600))
    usuario = show_login(screen)
    game = Game(usuario)
    game.run()

if __name__ == "__main__":
    main() 