import pygame
import time

def show_game_over(screen):
    global fondo_img
    fondo_img = pygame.transform.scale(pygame.image.load("assets/transicionNiveles/fondonegro3.jpg"), (screen.get_width(), screen.get_height()))
    # Renderizar el texto
    font = pygame.font.Font("assets/transicionNiveles/font2.ttf", 120)
    text = font.render('GAME OVER', True, (255,0,0))
    info = pygame.font.Font("assets/transicionNiveles/font4.TTF", 40).render('Presiona R para reiniciar o ESC para salir', True, (255,255,255))
    
    # Pintar la imagen de fondo
    screen.blit(fondo_img, (0, 0))
    
    # Dibujar el texto encima de la imagen
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
    global fondo_img
    fondo_img = pygame.transform.scale(pygame.image.load("assets/transicionNiveles/fondonegro3.jpg"), (screen.get_width(), screen.get_height()))
    # Renderizar el texto
    font = pygame.font.Font("assets/transicionNiveles/font2.ttf", 120)
    text = font.render('VICTORIA', True, (0,255,0))
    
    # Pintar la imagen de fondo
    screen.blit(fondo_img, (0, 0))
    
    # Dibujar el texto encima de la imagen
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
    
    pygame.display.flip()
    
    # Mostrar durante 3 segundos
    time.sleep(3)
