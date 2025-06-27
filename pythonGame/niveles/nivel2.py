from entities.enemy import Enemy
from entities.boss import Boss
from entities.life import Life
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
BARRAS_INVISIBLES = False

def cargar_nivel(game):
    # Música de fondo para el nivel 2
    pygame.mixer.music.load('soundtracks/Level2 OST.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)  # Cambia el volumen (0.0 a 1.0)
    game.enemies = []
    game.lives_drops = []  
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False
    game.boss_defeated = False
    game.barras = BARRAS
    game.barras_invisibles = BARRAS_INVISIBLES
    
    def spawn_enemy():
        enemy = game.spawn_enemy_far_from_player()
        game.enemies.append(enemy)

    # Spawnea los primeros enemigos
    for _ in range(5 + game.level):
        spawn_enemy()

    # Lógica de actualización del nivel 2
    def update_nivel2():
        # Spawnea nuevos enemigos hasta 40 kills
        while len(game.enemies) < (5 + game.level) and game.enemies_killed < 40 and not game.boss_spawned:
            spawn_enemy()
        # Spawnea jefe al matar 40 enemigos
        if game.enemies_killed >= 40 and not game.boss_spawned:
            game.boss = Boss(game.level, (1920, 1080))
            game.boss_spawned = True
            game.enemies.clear()  # Eliminar todos los enemigos restantes
        # Lógica del jefe
        if game.boss_spawned and game.boss:
            if hasattr(game.boss, 'lives') and game.boss.lives <= 0:
                game.boss = None
                game.level_completed = True
        # Recoger vidas
        for life in game.lives_drops[:]:
            if game.player.rect.colliderect(life.rect):
                game.player.lives += 1
                game.lives_drops.remove(life)
    game.update_nivel2 = update_nivel2

    # Hook para dropeo de vida: debe llamarse desde el sistema principal cuando se elimina un enemigo
    def drop_life_if_needed(x, y):
        if (game.enemies_killed > 0 and game.enemies_killed % 15 == 0):
            game.lives_drops.append(Life(x, y))
    game.drop_life_if_needed = drop_life_if_needed 