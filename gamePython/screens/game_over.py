import pygame
import time

def show_game_over(screen):
    font = pygame.font.SysFont(None, 80)
    text = font.render('GAME OVER', True, (255,0,0))
    info = pygame.font.SysFont(None, 40).render('Presiona R para reiniciar o ESC para salir', True, (255,255,255))
    screen.fill((0,0,0))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
    screen.blit(info, (screen.get_width()//2 - info.get_width()//2, screen.get_height()//2 + 60))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

def show_victory(screen):
    font = pygame.font.SysFont(None, 80)
    text = font.render('¡VICTORIA!', True, (0,255,0))
    screen.fill((0,0,0))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
    pygame.display.flip()
    time.sleep(3) 