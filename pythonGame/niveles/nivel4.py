from entities.enemy import Enemy
from entities.smart_enemy import SmartEnemy
from entities.trap import Trap
from entities.boss import Boss

def cargar_nivel(game):
    game.enemies = []
    game.smart_enemies = []
    game.traps = []
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False

    # Enemigos normales
    for _ in range(6 + game.level):
        enemy = game.spawn_enemy_far_from_player()
        game.enemies.append(enemy)

    # Enemigos inteligentes
    for _ in range(2 + game.level):
        smart_enemy = SmartEnemy(game.player)
        game.smart_enemies.append(smart_enemy)

    # Trampas en el mapa (posiciones fijas)
    game.traps.append(Trap(400, 300, 80, 30))
    game.traps.append(Trap(600, 200, 100, 40))

def update_level(game):
    # Actualizar enemigos inteligentes
    for smart_enemy in game.smart_enemies:
        smart_enemy.update(game.player)

    # Colisiones del jugador con trampas
    for trap in game.traps[:]:
        if trap.rect.colliderect(game.player.rect):
            game.player.lives -= 1
            game.traps.remove(trap)
            if game.player.lives <= 0:
                game.game_over = True

    # Verificar si debemos spawnear el jefe
    if not game.boss_spawned and game.enemies_killed >= 8:
        game.boss = Boss(game.level, (1920, 1080))
        game.boss_spawned = True
        game.enemies = []
        game.smart_enemies = []

    # Actualizar jefe si existe
    if game.boss:
        game.boss.update(game.player)
        for bullet in game.bullets[:]:
            if bullet.rect.colliderect(game.boss.rect):
                game.boss.lives -= 1
                game.bullets.remove(bullet)
                if game.boss.lives <= 0:
                    game.boss = None
                    game.level_completed = True





