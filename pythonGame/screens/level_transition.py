import pygame
import time

def show_level_transition(screen, level):
    font = pygame.font.SysFont(None, 80)
    text = font.render(f'Nivel {level}', True, (255,255,255))
    screen.fill((0,0,0))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
    pygame.display.flip()
    time.sleep(2) 