from entities.enemy import Enemy
import pygame

# Lista de barras de colisión: (x, y, ancho, alto)
# BARRAS 
# x: posición horizontal, y: posición vertical, ancho: tamaño horizontal, alto: tamaño vertical

#BARRAS 4 PAREDES

BARRAS = [
    pygame.Rect(20, 0, 40, 1080),    # Barra vertical izquierda
    pygame.Rect(1920-80, 0, 80, 1080),    # Barra vertical derecha más ancha
    pygame.Rect(0, 0, 1920, 200),    # Barra horizontal arriba más ancha
    pygame.Rect(0, 930, 1920, 180),    # Barra horizontal abajo más ancha hacia arriba

    
    pygame.Rect(1300, 700, 330, 100),    # TANQUE DERECHO
    pygame.Rect(220, 620, 250, 100),    # TANQUE IZQUIERDO

    pygame.Rect(785, 700, 350, 350),    # ESTRUCTURA CON ESTRELLA más grande y más arriba
]

# Variable para alternar visibilidad de las barras
BARRAS_INVISIBLES = True  # Cambia a True para hacerlas invisibles

def cargar_nivel(game):
    # Música de fondo para el nivel 1
    pygame.mixer.music.load('soundtracks/Level OST.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)  # Cambia el volumen (0.0 a 1.0)
    game.enemies = []
    game.enemies_killed = 0
    game.level_completed = False
    
    # Crear enemigos iniciales - mismo sistema que nivel 3
    for _ in range(6 + game.level):
        enemy = game.spawn_enemy_far_from_player()
        game.enemies.append(enemy)
    
    # Asigna las barras y la visibilidad al juego
    game.barras = BARRAS
    game.barras_invisibles = BARRAS_INVISIBLES

def update_level(game):
    """Lógica de actualización del nivel 1 - completar con 15 kills"""
    # Continuar spawneando enemigos hasta alcanzar 15 kills
    while len(game.enemies) < (6 + game.level) and game.enemies_killed < 15:
        enemy = game.spawn_enemy_far_from_player()
        game.enemies.append(enemy)
    
    # Completar nivel al matar 15 enemigos
    if game.enemies_killed >= 15:
        game.level_completed = True
        print(f"🎉 ¡NIVEL 1 COMPLETADO! Enemigos eliminados: {game.enemies_killed}") 