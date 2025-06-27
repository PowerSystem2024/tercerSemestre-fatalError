import random
from entities.enemy import Enemy4
from entities.smart_enemy import SmartEnemy
from entities.trap import Trap
from entities.boss import Boss, Boss4

def cargar_nivel(game):
    game.enemies = []
    game.smart_enemies = []
    game.traps = []
    game.boss = None
    game.enemies_killed = 0
    game.boss_spawned = False

    # Enemigos con ataques a distancia (Enemy4)
    for _ in range(4 + game.level):
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

    # Enemigos inteligentes (reducidos porque los Enemy4 son más peligrosos)
    for _ in range(1 + game.level//2):
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
        if trap.rect.colliderect(game.player.hitbox):
            hit_successful = game.player.hit()
            if hit_successful:
                game.traps.remove(trap)

    # Verificar si debemos spawnear el jefe
    if not game.boss_spawned and game.enemies_killed >= 8:
        print(f"🔥 SPAWNEANDO BOSS DEL NIVEL 4! Enemigos eliminados: {game.enemies_killed}")
        game.boss = Boss4(game.level, (1920, 1080))
        game.boss_spawned = True
        game.enemies = []
        game.smart_enemies = []
        print(f"✅ Boss spawneado con {game.boss.lives} vidas")

    # El jefe se actualiza en game.py, no aquí para evitar duplicación





