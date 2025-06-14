from entities.enemy import Enemy


def cargar_nivel(game):
    game.enemies = []
    cantidad = 9 + game.level * 2

    for _ in range(cantidad):
        enemy = game.spawn_enemy_far_from_player()
        enemy.speed = 1.0  # velocidad reducida (por defecto era 2 + level)
        game.enemies.append(enemy)
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