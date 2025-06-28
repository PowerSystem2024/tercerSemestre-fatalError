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
BARRAS_INVISIBLES = True
from entities.bullet import EnemyBullet

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
    for _ in range(6 + game.level):
        spawn_enemy()

    # Lógica de actualización del nivel 2
    def update_nivel2():
        # Spawnea nuevos enemigos hasta 15 kills
        while len(game.enemies) < (6 + game.level) and game.enemies_killed < 15 and not game.boss_spawned:
            spawn_enemy()
        # Spawnea jefe al matar 15 enemigos
        if game.enemies_killed >= 15 and not game.boss_spawned:
            game.boss = Boss(game.level, (1920, 1080))
            game.boss_spawned = True
            game.enemies.clear()  # Eliminar todos los enemigos restantes
            # --- INICIO TRAICIÓN ---
            from entities.enemy import Enemy2
            game.traitor_enemy = Enemy2(game.level, (1920, 1080))
            game.traitor_bullets = []
            game.enemies.append(game.traitor_enemy)
            game.traitor_active = True
            game.traitor_attack_cooldown = 0.5
            game.traitor_last_attack = 0
            game.traitor_lives = 10  # El traidor ahora tiene mucha más vida
            
        # Lógica del jefe
        if game.boss_spawned and game.boss:
            if hasattr(game.boss, 'lives') and game.boss.lives <= 0:
                game.boss = None
                game.level_completed = True
                game.traitor_active = False
                if hasattr(game, 'traitor_enemy') and game.traitor_enemy in game.enemies:
                    game.enemies.remove(game.traitor_enemy)
        # --- LÓGICA DE TRAICIÓN ---
        if getattr(game, 'traitor_active', False) and hasattr(game, 'traitor_enemy') and game.boss:
            traitor = game.traitor_enemy
            boss = game.boss
            import pygame, math
            now = pygame.time.get_ticks() / 1000.0
            # Movimiento evasivo mejorado: el traidor siempre intenta alejarse del jefe
            dx = boss.rect.centerx - traitor.rect.centerx
            dy = boss.rect.centery - traitor.rect.centery
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            distancia_peligro = 180
            distancia_optima = 350
            distancia_maxima = 500  # Distancia máxima permitida respecto al jefe
            if dist < distancia_peligro:
                # Si está en peligro, huir en línea recta
                traitor.rect.x -= int(traitor.speed * dx / dist * 1.5)
                traitor.rect.y -= int(traitor.speed * dy / dist * 1.5)
            elif dist < distancia_optima:
                # Si está cerca pero no en peligro, moverse lateralmente (esquivar)
                angle = math.atan2(dy, dx) + math.pi/2
                traitor.rect.x += int(math.cos(angle) * traitor.speed)
                traitor.rect.y += int(math.sin(angle) * traitor.speed)
            elif dist > distancia_maxima:
                # Si se aleja demasiado, orbitar alrededor del jefe en vez de huir más lejos
                angle = math.atan2(dy, dx) + math.pi/2
                traitor.rect.x += int(math.cos(angle) * traitor.speed * 0.7)
                traitor.rect.y += int(math.sin(angle) * traitor.speed * 0.7)
            else:
                # Si está lejos, solo orbita alrededor del jefe
                angle = math.atan2(dy, dx) + math.pi/2
                traitor.rect.x += int(math.cos(angle) * traitor.speed * 0.7)
                traitor.rect.y += int(math.sin(angle) * traitor.speed * 0.7)
            # Animación del traidor
            if abs(dx) > abs(dy):
                traitor.direction = 'right' if dx < 0 else 'left'
            else:
                traitor.direction = 'down' if dy < 0 else 'up'
            traitor.anim_timer += traitor.anim_speed
            if traitor.anim_timer >= 1:
                traitor.anim_index = (traitor.anim_index + 1) % len(traitor.animations[traitor.direction])
                traitor.anim_timer = 0
            traitor.image = traitor.animations[traitor.direction][traitor.anim_index]
            # El traidor dispara al jefe cada cierto tiempo
            if now - game.traitor_last_attack > game.traitor_attack_cooldown:
                bullet = EnemyBullet(traitor.rect.centerx, traitor.rect.centery, boss.rect.centerx, boss.rect.centery)
                game.traitor_bullets.append(bullet)
                game.traitor_last_attack = now
            # Actualizar balas del traidor
            for bullet in game.traitor_bullets[:]:
                if not bullet.update():
                    game.traitor_bullets.remove(bullet)
                elif bullet.rect.colliderect(boss.rect):
                    if hasattr(boss, 'take_damage'):
                        boss.take_damage(1)
                    else:
                        boss.lives -= 1
                    if bullet in game.traitor_bullets:
                        game.traitor_bullets.remove(bullet)
            # El jefe puede golpear al traidor si lo toca
            if traitor.rect.colliderect(boss.rect):
                game.traitor_lives -= 1
                traitor.rect.x -= int(dx / dist * 30)
                traitor.rect.y -= int(dy / dist * 30)
                if game.traitor_lives <= 0:
                    game.traitor_active = False
                    if traitor in game.enemies:
                        game.enemies.remove(traitor)
            # Limitar movimiento del traidor a los bordes del mapa
            traitor.rect.left = max(0, traitor.rect.left)
            traitor.rect.top = max(0, traitor.rect.top)
            traitor.rect.right = min(1920, traitor.rect.right)
            traitor.rect.bottom = min(1080, traitor.rect.bottom)
        
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