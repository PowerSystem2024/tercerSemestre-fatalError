from entities.enemy import Enemy

def cargar_nivel(game):
    game.enemies = []
    cantidad = 9 + game.level * 2

    for _ in range(cantidad):
        enemy = game.spawn_enemy_far_from_player()
        enemy.speed = 1.0  # velocidad reducida (por defecto era 2 + level)
        game.enemies.append(enemy)