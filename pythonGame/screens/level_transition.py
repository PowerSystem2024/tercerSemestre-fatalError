import pygame
import time

def show_level_transition(screen, level):
    screen.fill((30, 30, 30)) 

    # Carga y escala de imagen de fondo
    fondo_original = pygame.image.load("assets/transicionNiveles/imagenfondo.png")
    fondo = pygame.transform.scale(fondo_original, (screen.get_width(), screen.get_height()))

    # Fuente texto
    fuente = pygame.font.Font("assets/transicionNiveles/font5.ttf", 180)

    # Colores

    dorado = (218, 165, 32)
    blanco = (255, 255, 255)
    negro = (0, 0, 0)

    # Render de texto
    texto = fuente.render(f'Nivel {level}', True, dorado)
    x_final = (screen.get_width() - texto.get_width()) // 2
    y_text = (screen.get_height() - texto.get_height()) // 2
    x_text = -texto.get_width()  # Comienza fuera de la pantalla

    clock = pygame.time.Clock()

    # Slide-in animado 
    while x_text < x_final:
        screen.blit(fondo, (0, 0))

        # Borde blanco
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx != 0 or dy != 0:
                    borde = fuente.render(f'Nivel {level}', True, negro)
                    screen.blit(borde, (x_text + dx, y_text + dy))

        # Texto principal
        screen.blit(texto, (x_text, y_text))
        pygame.display.flip()
        clock.tick(60)
        x_text += 25  # Velocidad de entrada

    # Fade-in para que el texto brille 
    for alpha in range(0, 256, 15):
        screen.blit(fondo, (0, 0))

        # Borde blanco 
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx != 0 or dy != 0:
                    borde = fuente.render(f'Nivel {level}', True, negro)
                    screen.blit(borde, (x_final + dx, y_text + dy))

        # Texto principal con fade-in 
        texto_alpha = texto.copy()
        texto_alpha.set_alpha(alpha)
        screen.blit(texto_alpha, (x_final, y_text))

        pygame.display.flip()
        clock.tick(30)

    time.sleep(2)
