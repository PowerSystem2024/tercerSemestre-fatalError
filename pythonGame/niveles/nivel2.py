from entities.enemy import Enemy
from entities.boss import Boss
from entities.life import Life

def cargar_nivel(game):
    game.enemies = []
    game.lives_drops = []  
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False
    game.boss_defeated = False
    
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