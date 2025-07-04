import random
from entities.enemy import Enemy4
from entities.smart_enemy import SmartEnemy
from entities.trap import Trap
from entities.boss import Boss, Boss4
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
    # Música de fondo para el nivel 4
    pygame.mixer.music.load('soundtracks/Level4 OST.mp3')  # Cambia el archivo si quieres otra música
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)  # Cambia el volumen (0.0 a 1.0)
    game.enemies = []
    game.smart_enemies = []
    game.traps = []
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False
    game.barras = BARRAS
    game.barras_invisibles = BARRAS_INVISIBLES

    # Enemigos con ataques a distancia (Enemy4) - aumentar cantidad
    for _ in range(7 + game.level):  # Más enemigos iniciales (era 4)
        enemy = Enemy4(game.level, (1920, 1080))
        # Posicionar lejos del jugador
        while True:
            enemy.rect.x = random.randint(0, 1920 - enemy.rect.width)
            enemy.rect.y = random.randint(0, 1080 - enemy.rect.height)
            # Verificar que esté lejos del jugador
            dx = enemy.rect.centerx - game.player.rect.centerx
            dy = enemy.rect.centery - game.player.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            if distance > 400:  # Al menos 400 píxeles de distancia
                break
        game.enemies.append(enemy)

    # Enemigos inteligentes (aumentar cantidad)
    for _ in range(2 + game.level//2):  # Más enemigos inteligentes (era 1)
        smart_enemy = SmartEnemy(game.player)
        game.smart_enemies.append(smart_enemy)

    # Trampas en el mapa (posiciones fijas) - añadir más trampas
    game.traps.append(Trap(400, 300, 80, 30))
    game.traps.append(Trap(600, 200, 100, 40))
    game.traps.append(Trap(800, 500, 90, 35))  # Nueva trampa
    game.traps.append(Trap(1200, 400, 85, 32))  # Nueva trampa

def update_level(game):
    # Actualizar enemigos inteligentes
    for smart_enemy in game.smart_enemies:
        smart_enemy.update(game.player)

    # Colisiones del jugador con trampas
    for trap in game.traps[:]:
        if trap.rect.colliderect(game.player.hitbox):
            hit_successful = game.player.hit()
            if hit_successful:
                game.traps.remove(trap)

    # Continuar spawneando enemigos hasta alcanzar 20 kills
    while len(game.enemies) < (7 + game.level) and game.enemies_killed < 20 and not game.boss_spawned:
        enemy = Enemy4(game.level, (1920, 1080))
        # Posicionar lejos del jugador
        while True:
            enemy.rect.x = random.randint(0, 1920 - enemy.rect.width)
            enemy.rect.y = random.randint(0, 1080 - enemy.rect.height)
            dx = enemy.rect.centerx - game.player.rect.centerx
            dy = enemy.rect.centery - game.player.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            if distance > 400:
                break
        game.enemies.append(enemy)

    # Verificar si debemos spawnear el jefe - ahora a los 20 kills
    if not game.boss_spawned and game.enemies_killed >= 20:
        print(f"🔥 SPAWNEANDO BOSS DEL NIVEL 4! Enemigos eliminados: {game.enemies_killed}")
        game.boss = Boss4(game.level, (1920, 1080))
        game.boss_spawned = True
        game.enemies = []
        game.smart_enemies = []
        print(f"✅ Boss spawneado con {game.boss.lives} vidas")

    # El jefe se actualiza en game.py, no aquí para evitar duplicación





