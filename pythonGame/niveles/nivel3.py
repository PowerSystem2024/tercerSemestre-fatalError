from entities.enemy import Enemy
from entities.boss import Boss

def cargar_nivel(game):
    game.enemies = []
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False
    
    # Reducimos la cantidad de enemigos de 9 a 6
    for _ in range(6 + game.level):
        enemy = game.spawn_enemy_far_from_player()
        game.enemies.append(enemy)

def update_level(game):
    # Verificar si debemos spawnear el jefe
    if not game.boss_spawned and game.enemies_killed >= 6:  # Reducimos de 8 a 6 enemigos para spawnear el jefe
        game.boss = Boss(game.level, (1920, 1080))  # Usamos el tamaño del mapa directamente
        game.boss_spawned = True
        game.enemies = []  # Limpiar enemigos normales cuando aparece el jefe
    
    # Actualizar el jefe si existe
    if game.boss:
        game.boss.update(game.player)
        # Verificar colisiones con balas
        for bullet in game.bullets[:]:
            if bullet.rect.colliderect(game.boss.rect):
                game.boss.lives -= 1
                game.bullets.remove(bullet)
                if game.boss.lives <= 0:
                    game.boss = None
                    game.level_completed = True 