import random
from entities.enemy import Enemy3
from entities.boss import Boss3
import pygame

# BARRAS 
# x: posición horizontal, y: posición vertical, ancho: tamaño horizontal, alto: tamaño vertical
# BARRAS 4 PAREDES
BARRAS = [
    pygame.Rect(20, 0, 40, 1080),    # Barra vertical izquierda
    pygame.Rect(1920-80, 0, 80, 1080),    # Barra vertical derecha más ancha
    pygame.Rect(0, 0, 1920, 200),    # Barra horizontal arriba más ancha
    pygame.Rect(0, 930, 1920, 180),    # Barra horizontal abajo más ancha hacia arriba
    pygame.Rect(1300, 700, 330, 100),    # TANQUE DERECHO
    pygame.Rect(220, 620, 250, 100),    # TANQUE IZQUIERDO
    pygame.Rect(785, 700, 350, 350),    # ESTRUCTURA CON ESTRELLA más grande y más arriba
]
BARRAS_INVISIBLES = True

def cargar_nivel(game):
    # Música de fondo para el nivel 3
    pygame.mixer.music.load('soundtracks/Level3 OST.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)  # Cambia el volumen (0.0 a 1.0)
    game.barras = BARRAS
    game.barras_invisibles = BARRAS_INVISIBLES
    game.enemies = []
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False
    
    # Crear enemigos del nuevo tipo Enemy3
    for _ in range(6 + game.level):
        enemy = Enemy3(game.level, (1920, 1080))  # Crear Enemy3 directamente
        # Posicionar lejos del jugador
        while True:
            enemy.rect.x = random.randint(0, 1920 - enemy.rect.width)
            enemy.rect.y = random.randint(0, 1080 - enemy.rect.height)
            # Verificar que esté lejos del jugador
            dx = enemy.rect.centerx - game.player.rect.centerx
            dy = enemy.rect.centery - game.player.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            if distance > 300:  # Al menos 300 píxeles de distancia
                break
        game.enemies.append(enemy)
    
    # Asigna las barras y la visibilidad al juego
    game.barras = BARRAS
    game.barras_invisibles = BARRAS_INVISIBLES

def update_level(game):
    # Verificar si debemos spawnear el jefe
    if not game.boss_spawned and game.enemies_killed >= 15:  # Menos enemigos para que aparezca más rápido
        game.boss = Boss3(game.level, (1920, 1080))  # Usar el nuevo Boss3 mejorado
        game.boss_spawned = True
        game.enemies = []  # Limpiar enemigos normales cuando aparece el jefe
        print("🔥 ¡BOSS NIVEL 3 APARECE! Prepárate para la batalla!")
    
    # Actualizar el jefe si existe
    if game.boss:
        game.boss.update(game.player) 
    
    #esto es lo ultimo que hicimos dia miercoles 18 de junio