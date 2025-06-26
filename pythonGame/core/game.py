import pygame
from screens.level_transition import show_level_transition
from entities.player import Player
from entities.enemy import Enemy, Enemy2, Enemy3
from entities.bullet import Bullet
import random

WINDOW_SIZE = (1024, 576)  # Tamaño apropiado para notebooks
MAP_SIZE = (1920, 1080)    # Mapa original
BACKGROUND_SIZE = (1920, 1080)  # Fondo original

class Game:
    def _init_(self, username, level_manager, user_auth, initial_level_number, is_debug):
        self.username = username
        self.level_manager = level_manager
        self.user_auth = user_auth
        self.is_debug = is_debug
        self.screen = pygame.display.set_mode(WINDOW_SIZE)  # Ventana normal, no pantalla completa
        pygame.display.set_caption("Top Down Shooter")
        self.clock = pygame.time.Clock()
        self.max_level = 4
        self.running = True
        self.fullscreen = False
        self.background = pygame.image.load('assets/mapa/mapaUno.png').convert()
        self.background = pygame.transform.scale(self.background, BACKGROUND_SIZE)
        self.cursor_img = pygame.image.load('assets/cursor/cursor.png').convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (40, 40))
        pygame.mouse.set_visible(False)
        self.sangre_img = pygame.image.load('assets/muerte/sangre.png').convert_alpha()
        self.sangre_img = pygame.transform.scale(self.sangre_img, (60, 60))
        
        # Sistema de puntuación
        self.score = 0
        self.score_per_enemy = 100
        self.score_per_level = 500
        self.combo_multiplier = 1.0
        self.last_kill_time = 0
        self.combo_timeout = 2000  # 2 segundos para mantener combo
        
        # Cargar fuentes una sola vez para mejor rendimiento
        try:
            self.score_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 24)  # Más pequeño
            self.small_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 18)  # Más pequeño
        except:
            # Fallback si no encuentra las fuentes
            self.score_font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        
        # Cache para textos que no cambian frecuentemente
        self.cached_user_best = None
        self.cached_global_best = None
        self.cache_update_timer = 0
        
        # Inicializar el estado del juego para el primer nivel
        self._initialize_game_state(initial_level_number)

    def _initialize_game_state(self, level_number):
        self.level = level_number
        self.enemies_killed = 0
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.sangre_list = []
        self.boss = None
        self.boss_spawned = False
        self.level_completed = False

        user_data = self.user_auth.get_user_data(self.username)
        level_module = self.level_manager.load_level(self.level, user_data)
        if level_module:
            level_module.cargar_nivel(self)
        else:
            print(f"Could not load level {self.level}. Exiting game.")
            self.running = False

    def add_score(self, points):
        """Agregar puntos al score actual"""
        self.score += int(points * self.combo_multiplier)

    def update_combo(self):
        """Actualizar multiplicador de combo"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_kill_time < self.combo_timeout:
            self.combo_multiplier = min(self.combo_multiplier + 0.1, 3.0)  # Máximo 3x
        else:
            self.combo_multiplier = 1.0
        self.last_kill_time = current_time

    def spawn_enemy_far_from_player(self):
        while True:
            if self.level == 2:
                # 50% probabilidad de cada tipo
                if random.random() < 0.5:
                    enemy = Enemy(self.level, MAP_SIZE)
                else:
                    enemy = Enemy2(self.level, MAP_SIZE)
            elif self.level == 3:
                enemy = Enemy3(self.level, MAP_SIZE)
            else:
                enemy = Enemy(self.level, MAP_SIZE)
            dist = ((enemy.rect.centerx - self.player.rect.centerx) ** 2 + (enemy.rect.centery - self.player.rect.centery) ** 2) ** 0.5
            if dist > 400:
                return enemy

    def next_level(self):
        # Agregar puntos por completar nivel
        self.add_score(self.score_per_level)
        
        next_level_module = self.level_manager.next_level(self.username)
        if next_level_module:
            show_level_transition(self.screen, self.level_manager.get_current_level_number())
            self._initialize_game_state(self.level_manager.get_current_level_number())
        else:
            print("No more levels available.")
            from screens.game_over import show_victory
            show_victory(self.screen, self.user_auth, self.username, self.score)
            self.running = False

    def previous_level(self):
        prev_level_num = self.level - 1
        if prev_level_num > 0:
            self.level_manager.update_player_progress(self.username, prev_level_num)
            self._initialize_game_state(prev_level_num)
        else:
            print("Already at the first level.")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)

    def run(self):
        show_level_transition(self.screen, self.level)
        while self.running:
            self.clock.tick(60)
            
            # Calcular offset de la cámara
            cam_x = max(0, min(self.player.rect.centerx - WINDOW_SIZE[0]//2, MAP_SIZE[0] - WINDOW_SIZE[0]))
            cam_y = max(0, min(self.player.rect.centery - WINDOW_SIZE[1]//2, MAP_SIZE[1] - WINDOW_SIZE[1]))
            camera_offset = (cam_x, cam_y)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    if event.key == pygame.K_TAB:
                        # Mostrar ranking durante el juego
                        from screens.leaderboard import show_leaderboard
                        show_leaderboard(self.screen, self.user_auth, self.username)
                    if self.is_debug:
                        if event.key == pygame.K_n:
                            self.next_level()
                        if event.key == pygame.K_p:
                            self.previous_level()
                self.player.handle_event(event, self.bullets, camera_offset)
            self.update()
            self.draw()
            if self.player.lives <= 0:
                from screens.game_over import show_game_over
                restart = show_game_over(self.screen, self.user_auth, self.username, self.score)
                if restart:
                    self.score = 0  # Reiniciar puntuación
                    self._initialize_game_state(1)
                    show_level_transition(self.screen, self.level)
                else:
                    self.running = False
            if self.level == 3 and self.boss and self.boss.lives <= 0:
                self.next_level()
            elif self.level == 2 and self.level_completed:
                self.next_level()
            elif self.level != 2 and self.enemies_killed >= 20 and not self.boss_spawned:
                if self.level < self.max_level:
                    self.next_level()
                else:
                    from screens.game_over import show_victory
                    show_victory(self.screen, self.user_auth, self.username, self.score)
                    self.running = False

    def update(self):
        self.player.update(MAP_SIZE)
        for bullet in self.bullets[:]:
            bullet.update()
            # Verificar colisiones con enemigos normales
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.sangre_list.append((enemy.rect.centerx-30, enemy.rect.centery-30))
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.enemies_killed += 1
                    # Dropeo de vida solo en nivel 2
                    if self.level == 2 and hasattr(self, 'drop_life_if_needed'):
                        self.drop_life_if_needed(enemy.rect.centerx, enemy.rect.centery)
                    # Agregar puntos por matar enemigo
                    self.update_combo()
                    self.add_score(self.score_per_enemy)
                    break
            # Verificar colisiones con el jefe
            if self.boss and bullet.rect.colliderect(self.boss.rect):
                self.boss.lives -= 1
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if self.boss.lives <= 0:
                    self.boss = None
                    self.level_completed = True
                    # Agregar puntos por matar jefe
                    self.add_score(self.score_per_enemy * 5)  # 5x más puntos por jefe
                    # Si estamos en el nivel 3, pasar al siguiente nivel cuando se mata al jefe
                    if self.level == 3:
                        self.next_level()
                break

        # Actualizar enemigos normales
        for enemy in self.enemies[:]:
            enemy.update(self.player)
            # Solo los enemigos que no son Enemy3 causan daño por contacto
            # Los Enemy3 atacan con su sistema de ataque propio
            if not isinstance(enemy, type(self.enemies[0])) or not hasattr(enemy, 'is_attacking'):
                if enemy.rect.colliderect(self.player.hitbox):
                    hit_successful = self.player.hit()
                    if hit_successful and enemy in self.enemies:
                        self.enemies.remove(enemy)

        # Actualizar jefe
        if self.boss:
            self.boss.update(self.player)
            if self.boss.rect.colliderect(self.player.hitbox):
                self.player.hit()
                
        # INICIO NIVEL 2
        if self.level == 2:
            if hasattr(self, 'update_nivel2'):
                self.update_nivel2()
            return
        
        # Spawnear más enemigos si es necesario
        if self.level == 3:
            if not self.boss_spawned:
                while len(self.enemies) < (5 + self.level*2):
                    self.enemies.append(self.spawn_enemy_far_from_player())
        else:
            while len(self.enemies) < (5 + self.level*2):
                self.enemies.append(self.spawn_enemy_far_from_player())

        # Actualizar nivel 3
        if self.level == 3:
            from niveles import nivel3
            nivel3.update_level(self)

    def draw(self):
        cam_x = max(0, min(self.player.rect.centerx - WINDOW_SIZE[0]//2, MAP_SIZE[0] - WINDOW_SIZE[0]))
        cam_y = max(0, min(self.player.rect.centery - WINDOW_SIZE[1]//2, MAP_SIZE[1] - WINDOW_SIZE[1]))
        camera = pygame.Rect(cam_x, cam_y, WINDOW_SIZE[0], WINDOW_SIZE[1])
        map_surface = self.background.copy()
        for pos in self.sangre_list:
            map_surface.blit(self.sangre_img, pos)
        self.player.draw(map_surface)
        for enemy in self.enemies:
            enemy.draw(map_surface)
        if self.boss:
            self.boss.draw(map_surface)
        for bullet in self.bullets:
            bullet.draw(map_surface)
         # INICIO VIDAS DROPEADAS NIVEL 2
        if self.level == 2 and hasattr(self, 'lives_drops'):
            for life in self.lives_drops:
                life.draw(map_surface)
        self.screen.blit(map_surface, (0,0), camera)
        
        # HUD
        self.draw_score_info()
        # VIDAS SIEMPRE ARRIBA DE TODO
        self.player.draw_lives(self.screen)
        # Cursor
        mx, my = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, (mx-20, my-20))
        pygame.display.flip()

    def draw_score_info(self):
        """Dibujar información de puntuación en la pantalla, ahora en la esquina inferior derecha, pequeño y estético"""
        hud_width = 250
        hud_height = 120
        margin = 18
        hud_x = WINDOW_SIZE[0] - hud_width - margin
        hud_y = WINDOW_SIZE[1] - hud_height - margin
        info_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
        info_surface.set_alpha(120)
        pygame.draw.rect(info_surface, (0, 0, 0, 180), (0, 0, hud_width, hud_height), border_radius=14)
        pygame.draw.rect(info_surface, (255, 255, 255, 30), (0, 0, hud_width, hud_height), 2, border_radius=14)
        x_text = 16
        y_text = 12
        line_space = 24
        # Score
        score_text = self.score_font.render(f'Score: {self.score}', True, (230, 230, 230))
        shadow = self.score_font.render(f'Score: {self.score}', True, (40, 40, 40))
        info_surface.blit(shadow, (x_text+1, y_text+1))
        info_surface.blit(score_text, (x_text, y_text))
        # Nivel
        level_text = self.score_font.render(f'Nivel: {self.level}', True, (173, 216, 230))
        shadow = self.score_font.render(f'Nivel: {self.level}', True, (40, 40, 40))
        info_surface.blit(shadow, (x_text+1, y_text + line_space+1))
        info_surface.blit(level_text, (x_text, y_text + line_space))
        # Enemigos eliminados
        enemies_text = self.score_font.render(f'Enemigos: {self.enemies_killed}', True, (255, 182, 193))
        shadow = self.score_font.render(f'Enemigos: {self.enemies_killed}', True, (40, 40, 40))
        info_surface.blit(shadow, (x_text+1, y_text + 2*line_space+1))
        info_surface.blit(enemies_text, (x_text, y_text + 2*line_space))
        # Combo
        if self.combo_multiplier > 1.0:
            combo_text = self.score_font.render(f'Combo: x{self.combo_multiplier:.1f}', True, (255, 215, 0))
            shadow = self.score_font.render(f'Combo: x{self.combo_multiplier:.1f}', True, (80, 80, 0))
            info_surface.blit(shadow, (x_text+1, y_text + 3*line_space+1))
            info_surface.blit(combo_text, (x_text, y_text + 3*line_space))
        self.screen.blit(info_surface, (hud_x, hud_y))
        
        # Actualizar cache cada 5 segundos para evitar consultas constantes a la BD
        current_time = pygame.time.get_ticks()
        if current_time - self.cache_update_timer > 5000:  # 5 segundos
            try:
                user_data = self.user_auth.get_user_data(self.username)
                self.cached_user_best = user_data.get("high_score", 0) if user_data else 0
                
                best_score = self.user_auth.get_best_score()
                self.cached_global_best = best_score.get("high_score", 0) if best_score else 0
            except:
                # Si hay error en la BD, usar valores por defecto
                self.cached_user_best = 0
                self.cached_global_best = 0
            self.cache_update_timer = current_time
        
        pygame.display.flip()