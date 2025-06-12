from entities.enemy import Enemy

def cargar_nivel(game):
    game.enemies = []
    for _ in range(12 + game.level*2):
        enemy = game.spawn_enemy_far_from_player()
        game.enemies.append(enemy) 