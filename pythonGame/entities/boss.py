import pygame
from entities.enemy import Enemy
from entities.bullet import EnemyBullet
from utils.spritesheet import SpriteSheet
import math
import random

class Boss(Enemy):
    def __init__(self, level, map_size, pos=None):
        super().__init__(level, map_size, pos)
        self.spritesheet = SpriteSheet('assets/enemigos/enemigos2.png', 'assets/enemigos/enemigos2.plist', scale=0.7)
        self.animations = {
            'down': self.spritesheet.get_images_by_range(0, 4),
            'left': self.spritesheet.get_images_by_range(4, 8),
            'right': self.spritesheet.get_images_by_range(8, 12),
            'up': self.spritesheet.get_images_by_range(12, 16)
        }
        self.image = self.animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.center = (map_size[0]//2, map_size[1]//2)
        self.speed = 1.5 + (level * 0.3)  # Velocidad más razonable
        self.lives = 8  # Más vidas para mayor desafío
        self.max_lives = 8  # Para calcular la barra de vida
        
        # Sistema de poder especial para nivel 2
        self.power_active = False
        self.power_timer = 0
        self.power_duration = 7.0  # 7 segundos de poder (más tiempo)
        self.power_cooldown = 6.0  # 6 segundos entre poderes (menos cooldown)
        self.last_power_time = 0
        self.resistance_multiplier = 1.0  # Multiplicador de resistencia
        
        # Cargar imagen del poder especial
        try:
            self.power_image = pygame.image.load('assets/enemigos/ataques/PoderBossNivel2.png').convert_alpha()
            self.power_image = pygame.transform.scale(self.power_image, (int(self.rect.width * 0.7), int(self.rect.height * 0.7)))
            print("✅ Imagen PoderBossNivel2.png cargada correctamente")
        except Exception as e:
            print(f"❌ No se pudo cargar PoderBossNivel2.png: {e}")
            self.power_image = None
        
        # Imagen original para restaurar
        self.original_image = self.image.copy()

    def update(self, player):
        # Llamar al update de la clase padre (Enemy)
        super().update(player)
        
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Sistema de poder especial
        if not self.power_active and current_time - self.last_power_time >= self.power_cooldown:
            # Activar poder
            self.activate_power()
            self.last_power_time = current_time
        
        if self.power_active:
            self.power_timer += 1/60.0  # Incrementar timer (asumiendo 60 FPS)
            
            if self.power_timer >= self.power_duration:
                # Desactivar poder
                self.deactivate_power()
        
        # --- MODIFICACIÓN: El jefe puede perseguir al traidor si está activo ---
        traitor = getattr(player, 'traitor_enemy', None)
        traitor_active = getattr(player, 'traitor_active', False)
        if traitor and traitor_active:
            # Elegir objetivo más cercano: jugador o traidor
            dx_p = player.rect.centerx - self.rect.centerx
            dy_p = player.rect.centery - self.rect.centery
            dist_p = (dx_p**2 + dy_p**2) ** 0.5
            dx_t = traitor.rect.centerx - self.rect.centerx
            dy_t = traitor.rect.centery - self.rect.centery
            dist_t = (dx_t**2 + dy_t**2) ** 0.5
            if dist_t < dist_p:
                # Perseguir al traidor
                self.intelligent_movement(traitor)
            else:
                self.intelligent_movement(player)
        else:
            self.intelligent_movement(player)
    
    def intelligent_movement(self, player):
        """Movimiento inteligente del boss"""
        # Calcular distancia al jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        
        if self.power_active:
            # Con poder: más agresivo, persigue directamente
            if distance > 120:  # Mantener distancia de ataque
                move_x = (dx / distance) * self.speed * 0.8  # Reducir velocidad
                move_y = (dy / distance) * self.speed * 0.8
                self.rect.x += int(move_x)
                self.rect.y += int(move_y)
        else:
            # Sin poder: más cauteloso, movimiento evasivo
            if distance < 180:
                # Demasiado cerca, retroceder
                move_x = -(dx / distance) * self.speed * 0.5
                move_y = -(dy / distance) * self.speed * 0.5
            elif distance > 350:
                # Muy lejos, acercarse
                move_x = (dx / distance) * self.speed * 0.7
                move_y = (dy / distance) * self.speed * 0.7
            else:
                # Distancia óptima, movimiento lateral
                import math
                angle = math.atan2(dy, dx) + math.pi/2  # Perpendicular
                move_x = math.cos(angle) * self.speed * 0.6
                move_y = math.sin(angle) * self.speed * 0.6
            
            self.rect.x += int(move_x)
            self.rect.y += int(move_y)
        
        # Mantener dentro del mapa
        self.rect.clamp_ip(pygame.Rect(0, 0, 1920, 1080))

    def activate_power(self):
        """Activa el poder especial del boss"""
        self.power_active = True
        self.power_timer = 0
        self.resistance_multiplier = 0.15  # Toma solo el 15% del daño (MUCHO más resistente)
        self.speed *= 1.2  # Solo 20% más rápido (antes era 50%)
        
        # Cambiar imagen al poder especial si está disponible
        if self.power_image:
            self.image = self.power_image
        
        print("🔥 ¡BOSS ACTIVÓ PODER DE RESISTENCIA EXTREMA! Resistencia x6.7")

    def deactivate_power(self):
        """Desactiva el poder especial del boss"""
        self.power_active = False
        self.power_timer = 0
        self.resistance_multiplier = 1.0  # Daño normal
        self.speed /= 1.2  # Restaurar velocidad normal
        
        # Restaurar imagen original
        self.image = self.original_image
        
        print("💨 Poder de resistencia desactivado - Boss vulnerable")

    def take_damage(self, damage=1):
        """Método personalizado para recibir daño con resistencia"""
        if self.power_active:
            # Con poder: muy resistente pero no invulnerable
            # Solo 1 de cada 5 disparos hace daño
            import random
            if random.random() < 0.2:  # 20% de probabilidad de hacer daño
                self.lives -= 1
                print(f"🛡️💥 Boss con poder recibió daño! Vidas: {self.lives}")
                return True
            else:
                print(f"🛡️ ¡ATAQUE BLOQUEADO POR EL PODER!")
                return False
        else:
            # Sin poder, daño normal - siempre hace daño
            self.lives -= 1
            print(f"💥 Boss vulnerable recibió daño. Vidas: {self.lives}")
            return True

    def draw(self, surface):
        # Dibujar el boss
        surface.blit(self.image, self.rect)
        
        # Dibujar indicador visual cuando el poder está activo
        if self.power_active:
            # Efecto de brillo/aura alrededor del boss
            glow_size = 10
            glow_color = (255, 100, 100, 100)  # Rojo semi-transparente
            
            # Crear superficie temporal para el efecto
            glow_surface = pygame.Surface((self.rect.width + glow_size*2, self.rect.height + glow_size*2), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect(), glow_size)
            
            surface.blit(glow_surface, (self.rect.x - glow_size, self.rect.y - glow_size))
        
        # Dibujar barra de vida para todos los bosses
        if self.lives > 0:
            bar_width = 250
            bar_height = 25
            bar_x = surface.get_width() // 2 - bar_width // 2
            bar_y = 40
            
            # Fondo de la barra (más oscuro)
            pygame.draw.rect(surface, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Barra de vida actual
            current_width = int((self.lives / self.max_lives) * bar_width)
            if self.power_active:
                # Barra brillante cuando tiene poder
                color = (255, 50, 50)
                # Efecto de pulso
                pulse = int(50 * (1 + 0.3 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() * 0.3).x))
                color = (min(255, 255), min(255, 50 + pulse), min(255, 50 + pulse))
            else:
                color = (200, 0, 0)
            pygame.draw.rect(surface, color, (bar_x, bar_y, current_width, bar_height))
            
            # Borde brillante
            border_color = (255, 255, 100) if self.power_active else (255, 255, 255)
            pygame.draw.rect(surface, border_color, (bar_x, bar_y, bar_width, bar_height), 3)
            
            # Texto del boss
            font = pygame.font.Font(None, 32)
            if self.power_active:
                text_color = (255, 255, 100)
                status_text = " ⚡ RESISTENCIA EXTREMA ⚡"
            else:
                text_color = (255, 255, 255)
                status_text = ""
            
            # Determinar nivel del boss
            if hasattr(self, 'level'):
                level_text = f"BOSS NIVEL {self.level}"
            else:
                level_text = "BOSS"
                
            text = font.render(f"{level_text}{status_text}", True, text_color)
            text_rect = text.get_rect(center=(surface.get_width() // 2, bar_y - 25))
            surface.blit(text, text_rect)
            
            # Mostrar vidas numéricamente
            lives_text = font.render(f"{self.lives}/{self.max_lives}", True, text_color)
            lives_rect = lives_text.get_rect(center=(surface.get_width() // 2, bar_y + bar_height + 15))
            surface.blit(lives_text, lives_rect)

class Boss3(Boss):
    """Boss especializado para el nivel 3 - Táctico con ataques sorpresivos"""
    def __init__(self, level, map_size, pos=None):
        # No llamar super().__init__ para evitar cargar sprites incorrectos
        # Cargar spritesheet de enemigos nivel 3
        self.spritesheet = SpriteSheet('assets/enemigos/nenemigos3.png', 'assets/enemigos/nenemigos3.plist', scale=1.8)
        # Spritesheet para ataques
        self.attack_spritesheet = SpriteSheet('assets/enemigos/ataques/ataque-enemigo-3.png', 'assets/enemigos/ataques/ataque-enemigo-3.plist', scale=1.8)
        
        # Animaciones de movimiento usando los nombres específicos del plist
        self.move_animations = {
            'down': [
                self.spritesheet.get_image_by_name('abajo1.png'),
                self.spritesheet.get_image_by_name('abajo2.png'),
                self.spritesheet.get_image_by_name('abajo3.png'),
                self.spritesheet.get_image_by_name('abajo4.png')
            ],
            'left': [
                self.spritesheet.get_image_by_name('izquierda1.png'),
                self.spritesheet.get_image_by_name('izquierda2.png'),
                self.spritesheet.get_image_by_name('izquierda3.png'),
                self.spritesheet.get_image_by_name('izquierda4.png')
            ],
            'right': [
                self.spritesheet.get_image_by_name('derecha1.png'),
                self.spritesheet.get_image_by_name('derecha2.png'),
                self.spritesheet.get_image_by_name('derecha3.png'),
                self.spritesheet.get_image_by_name('derecha4.png')
            ],
            'up': [
                self.spritesheet.get_image_by_name('arriba1.png'),
                self.spritesheet.get_image_by_name('arriba2.png'),
                self.spritesheet.get_image_by_name('arriba3.png'),
                self.spritesheet.get_image_by_name('arriba4.png')
            ]
        }
        
        # Animaciones de ataque
        self.attack_animations = {
            'down': [
                self.attack_spritesheet.get_image_by_name('abajoataque1.png'),
                self.attack_spritesheet.get_image_by_name('abajoataque2.png'),
                self.attack_spritesheet.get_image_by_name('abajoataque3.png'),
                self.attack_spritesheet.get_image_by_name('abajoataque4.png')
            ],
            'left': [
                self.attack_spritesheet.get_image_by_name('ataqueizquierda1.png'),
                self.attack_spritesheet.get_image_by_name('ataqueizquierda2.png'),
                self.attack_spritesheet.get_image_by_name('ataqueizquierda3.png'),
                self.attack_spritesheet.get_image_by_name('ataqueizquierda4.png')
            ],
            'right': [
                self.attack_spritesheet.get_image_by_name('ataquederecha1.png'),
                self.attack_spritesheet.get_image_by_name('ataquederecha2.png'),
                self.attack_spritesheet.get_image_by_name('ataquederecha3.png'),
                self.attack_spritesheet.get_image_by_name('ataquederecha4.png')
            ],
            'up': [
                self.attack_spritesheet.get_image_by_name('ataquearriba1.png'),
                self.attack_spritesheet.get_image_by_name('ataquearriba2.png'),
                self.attack_spritesheet.get_image_by_name('ataquearriba3.png'),
                self.attack_spritesheet.get_image_by_name('ataquearriba4.png')
            ]
        }
        
        # Inicializar propiedades básicas
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.15
        self.image = self.move_animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.center = (map_size[0]//2, map_size[1]//2)
        
        # Boss del nivel 3 es más fuerte y ágil
        self.lives = 15  # Más vidas que antes (era 10)
        self.max_lives = 15
        self.base_speed = 2.5  # Más ágil que antes (era 1.5 * 0.8)
        self.speed = self.base_speed
        
        # Sistema de ataques sorpresivos mejorado
        self.dash_cooldown_min = 3.0  # Más frecuente (era 4.0)
        self.dash_cooldown_max = 6.0  # Más frecuente (era 8.0)
        self.current_dash_cooldown = self.get_random_cooldown()
        self.last_dash_time = 0
        self.dashing = False
        self.dash_duration = 1.0  # Dash más largo (era 0.8)
        self.dash_timer = 0
        self.dash_speed = self.base_speed * 4.0  # Más rápido durante dash (era 3.5x)
        
        # Sistema de ataque especial
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.6  # Duración del ataque
        self.attack_cooldown = 4.0  # Cooldown entre ataques especiales
        self.last_attack_time = 0
        
        # Patrón de movimiento táctico
        self.movement_timer = 0
        self.movement_phase = 0  # 0: lento, 1: dash, 2: attack
        
        print("🔥 BOSS NIVEL 3 MEJORADO - Skin nenemigos3 con ataques especiales!")

    def get_random_cooldown(self):
        """Genera un cooldown aleatorio para el dash"""
        import random
        return random.uniform(self.dash_cooldown_min, self.dash_cooldown_max)
        
    def update(self, player):
        current_time = pygame.time.get_ticks() / 1000.0
        self.movement_timer += 1/60.0
        
        # Calcular dirección hacia el jugador para animaciones
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        
        # Determinar dirección para animación
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'
        
        # Sistema de ataque especial
        if not self.attacking and not self.dashing and current_time - self.last_attack_time >= self.attack_cooldown:
            if distance < 150:  # Rango de ataque cercano
                self.start_attack()
                self.last_attack_time = current_time
        
        # Sistema de dash sorpresivo
        if not self.dashing and not self.attacking and current_time - self.last_dash_time >= self.current_dash_cooldown:
            if 200 < distance < 400:  # Solo dash si está a distancia media
                self.start_dash(player)
                self.last_dash_time = current_time
                self.current_dash_cooldown = self.get_random_cooldown()
        
        # Ejecutar estados
        if self.attacking:
            self.execute_attack()
        elif self.dashing:
            self.execute_dash()
        else:
            # Movimiento táctico normal
            self.tactical_movement(player)
        
        # Actualizar animaciones
        self.anim_timer += self.anim_speed
        if self.anim_timer >= 1:
            if self.attacking:
                self.anim_index = (self.anim_index + 1) % len(self.attack_animations[self.direction])
                self.image = self.attack_animations[self.direction][self.anim_index]
            else:
                self.anim_index = (self.anim_index + 1) % len(self.move_animations[self.direction])
                self.image = self.move_animations[self.direction][self.anim_index]
            self.anim_timer = 0
    
    def start_dash(self, player):
        """Inicia un dash sorpresivo hacia el jugador"""
        self.dashing = True
        self.dash_timer = 0
        self.speed = self.dash_speed  # Cambiar a velocidad de dash
        
        # Calcular dirección del dash hacia el jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        self.dash_direction_x = dx / distance
        self.dash_direction_y = dy / distance
        
        print("⚡ BOSS NIVEL 3 DASH SORPRESIVO!")
    
    def start_attack(self):
        """Inicia un ataque especial"""
        self.attacking = True
        self.attack_timer = 0
        self.anim_index = 0  # Reiniciar animación de ataque
        print("💥 BOSS NIVEL 3 ATAQUE ESPECIAL!")
    
    def execute_attack(self):
        """Ejecuta el ataque especial"""
        self.attack_timer += 1/60.0
        
        if self.attack_timer >= self.attack_duration:
            # Terminar ataque
            self.attacking = False
            self.anim_index = 0  # Reiniciar para animación de movimiento
            print("✨ Ataque especial completado")
    
    def get_attack_rect(self):
        """Devuelve el rectángulo de ataque cuando está atacando"""
        if self.attacking and self.attack_timer > 0.2:  # Después de un pequeño delay
            # Crear rectángulo de ataque más grande que el boss
            attack_size = 80
            attack_rect = pygame.Rect(0, 0, attack_size, attack_size)
            attack_rect.center = self.rect.center
            return attack_rect
        return None
    
    def execute_dash(self):
        """Ejecuta el dash rápido"""
        self.dash_timer += 1/60.0
        
        # Moverse en la dirección del dash
        move_x = self.dash_direction_x * self.speed
        move_y = self.dash_direction_y * self.speed
        self.rect.x += int(move_x)
        self.rect.y += int(move_y)
        
        # Mantener dentro del mapa durante el dash
        self.rect.clamp_ip(pygame.Rect(0, 0, 1920, 1080))
        
        if self.dash_timer >= self.dash_duration:
            # Terminar dash
            self.dashing = False
            self.speed = self.base_speed  # Volver a velocidad lenta
            print("💨 Dash completado - Boss vuelve a modo táctico")
    
    def draw(self, surface):
        # Dibujar el boss con la nueva skin
        surface.blit(self.image, self.rect)
        
        # Dibujar barra de vida del boss
        if self.lives > 0:
            bar_width = 250
            bar_height = 25
            bar_x = surface.get_width() // 2 - bar_width // 2
            bar_y = 40
            
            # Fondo de la barra
            pygame.draw.rect(surface, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Barra de vida actual
            current_width = int((self.lives / self.max_lives) * bar_width)
            color = (255, 150, 0)  # Naranja para Boss3
            pygame.draw.rect(surface, color, (bar_x, bar_y, current_width, bar_height))
            
            # Borde
            pygame.draw.rect(surface, (255, 215, 0), (bar_x, bar_y, bar_width, bar_height), 3)
            
            # Texto del boss
            font = pygame.font.Font(None, 32)
            text = font.render("⚔️ BOSS NIVEL 3 - GUERRERO ⚔️", True, (255, 150, 0))
            text_rect = text.get_rect(center=(surface.get_width() // 2, bar_y - 25))
            surface.blit(text, text_rect)
        
        # Efecto visual durante el ataque
        if self.attacking:
            # Crear efecto de ataque brillante
            attack_color = (255, 255, 100, 180)  # Amarillo brillante
            attack_size = 25
            
            # Dibujar aura de ataque
            attack_surface = pygame.Surface((attack_size*4, attack_size*4), pygame.SRCALPHA)
            pygame.draw.circle(attack_surface, attack_color, (attack_size*2, attack_size*2), attack_size*2)
            surface.blit(attack_surface, (self.rect.centerx - attack_size*2, self.rect.centery - attack_size*2))
        
        # Efecto visual durante el dash
        if self.dashing:
            # Crear efecto de estela/velocidad
            trail_color = (255, 100, 100, 150)  # Rojo semi-transparente
            trail_size = 15
            
            # Dibujar múltiples círculos para simular estela
            for i in range(3):
                offset = i * 20  # Separación entre círculos de estela
                trail_surface = pygame.Surface((trail_size*2, trail_size*2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, trail_color, (trail_size, trail_size), trail_size - i*3)
                surface.blit(trail_surface, (self.rect.centerx - trail_size - offset, self.rect.centery - trail_size))
    
    def tactical_movement(self, player):
        """Movimiento táctico lento similar al Boss4"""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        
        # Patrón de movimiento similar al Boss4 pero más simple
        if self.movement_timer < 4.0:
            # Fase 1: Acercarse lentamente (4 segundos)
            if distance > 180:  # Mantener distancia táctica
                move_x = (dx / distance) * self.speed * 0.6
                move_y = (dy / distance) * self.speed * 0.6
                self.rect.x += int(move_x)
                self.rect.y += int(move_y)
        else:
            # Fase 2: Movimiento lateral/evasivo (2 segundos)
            if self.movement_timer >= 6.0:
                self.movement_timer = 0  # Reiniciar ciclo
            
            # Movimiento lateral para evitar disparos
            import math
            angle = math.atan2(dy, dx) + math.pi/2  # Perpendicular al jugador
            move_x = math.cos(angle) * self.speed * 0.5
            move_y = math.sin(angle) * self.speed * 0.5
            self.rect.x += int(move_x)
            self.rect.y += int(move_y)
        
        # Mantener dentro del mapa
        self.rect.clamp_ip(pygame.Rect(0, 0, 1920, 1080))

class Boss4:
    def __init__(self, level, map_size, pos=None):
        # Cargar imagen única del boss del nivel 4
        try:
            self.original_image = pygame.image.load('assets/enemigos/BossNivel4.png').convert_alpha()
            # Escalar el boss para que se vea imponente
            self.original_image = pygame.transform.scale(self.original_image, (120, 120))
            print("✅ Imagen BossNivel4.png cargada correctamente")
        except Exception as e:
            # Fallback: crear un boss simple si no encuentra la imagen
            self.original_image = pygame.Surface((100, 100))
            self.original_image.fill((150, 0, 0))  # Rojo oscuro
            print(f"❌ No se pudo cargar BossNivel4.png: {e}")
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.center = (map_size[0]//2, map_size[1]//2)
        
        # Estadísticas del boss
        self.speed = 1.5  # Más lento pero más peligroso
        self.lives = 30  # Extremadamente resistente (era 20)
        self.max_lives = 30  # Para la barra de vida
        self.direction = 'down'
        
        # Sistema de resistencia
        self.resistance_active = False
        self.resistance_timer = 0
        self.resistance_duration = 10.0  # 10 segundos de resistencia (era 8)
        self.resistance_cooldown = 3.0  # Solo 3 segundos entre activaciones (era 5)
        self.last_resistance_time = 0
        
        # Sistema de ataque múltiple
        self.bullets = []
        self.last_attack_time = 0
        self.attack_cooldown = 1.5  # Ataca cada 1.5 segundos
        self.attack_range = 300  # Rango largo de ataque
        
        # Patrón de movimiento
        self.movement_timer = 0
        self.movement_pattern = 0  # 0: hacia jugador, 1: circular
        self.center_x = map_size[0] // 2
        self.center_y = map_size[1] // 2
        
        # Cargar sonido de disparo si existe
        try:
            self.shoot_sound = pygame.mixer.Sound('sonidos/BossApear.wav')
        except:
            self.shoot_sound = None

    def update(self, player):
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Actualizar balas del boss
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]
        
        # Sistema de resistencia
        if not self.resistance_active and current_time - self.last_resistance_time >= self.resistance_cooldown:
            # Activar resistencia más frecuentemente - cuando tenga 80% o menos vida
            if self.lives <= self.max_lives * 0.8:  # Cuando tenga 80% o menos vida (era 60%)
                self.activate_resistance()
                self.last_resistance_time = current_time
        
        if self.resistance_active:
            self.resistance_timer += 1/60.0
            if self.resistance_timer >= self.resistance_duration:
                self.deactivate_resistance()
        
        # Patrón de movimiento alternativo
        self.movement_timer += 1/60.0
        
        if self.movement_timer < 3.0:
            # Fase 1: Perseguir al jugador (3 segundos)
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            
            if dist > 200:  # Mantener cierta distancia
                self.rect.x += int(self.speed * dx / dist)
                self.rect.y += int(self.speed * dy / dist)
        else:
            # Fase 2: Movimiento circular (2 segundos)
            if self.movement_timer >= 5.0:
                self.movement_timer = 0  # Reiniciar ciclo
            
            # Movimiento circular alrededor del centro
            angle = (self.movement_timer - 3.0) * 2  # Velocidad del círculo
            radius = 150
            target_x = self.center_x + math.cos(angle) * radius
            target_y = self.center_y + math.sin(angle) * radius
            
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            self.rect.x += int(dx * 0.02)  # Movimiento suave
            self.rect.y += int(dy * 0.02)
        
        # Sistema de ataque
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.attack_player(player)
            self.last_attack_time = current_time

    def attack_player(self, player):
        """Ataque múltiple del boss"""
        # Disparar 3 balas en un patrón de abanico
        for i in range(3):
            angle_offset = (i - 1) * 0.3  # Ángulos: -0.3, 0, 0.3 radianes
            
            # Calcular ángulo base hacia el jugador
            base_angle = math.atan2(player.rect.centery - self.rect.centery, 
                                  player.rect.centerx - self.rect.centerx)
            
            # Aplicar offset para crear abanico
            final_angle = base_angle + angle_offset
            
            # Calcular posición objetivo
            distance = 500  # Distancia del disparo
            target_x = self.rect.centerx + math.cos(final_angle) * distance
            target_y = self.rect.centery + math.sin(final_angle) * distance
            
            # Crear bala
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, target_x, target_y)
            self.bullets.append(bullet)
        
        if self.shoot_sound:
            self.shoot_sound.play()

    def activate_resistance(self):
        """Activa la resistencia del boss final - ahora más poderosa"""
        self.resistance_active = True
        self.resistance_timer = 0
        self.speed *= 1.5  # Más rápido durante resistencia (era 1.3)
        self.attack_cooldown *= 0.7  # Ataca más frecuentemente durante resistencia
        print("🔥🛡️ BOSS FINAL ACTIVÓ RESISTENCIA SUPREMA! ¡CASI INVENCIBLE!")

    def deactivate_resistance(self):
        """Desactiva la resistencia del boss final"""
        self.resistance_active = False
        self.resistance_timer = 0
        self.speed /= 1.5  # Restaurar velocidad
        self.attack_cooldown /= 0.7  # Restaurar velocidad de ataque
        print("💨 Resistencia Suprema desactivada - Boss Final temporalmente vulnerable")

    def take_damage(self, damage=1):
        """Método personalizado para recibir daño con resistencia extrema"""
        if self.resistance_active:
            # Con resistencia: extremadamente resistente
            import random
            if random.random() < 0.15:  # Solo 15% de probabilidad de hacer daño (era 25%)
                self.lives -= 1
                print(f"🛡️💥 Boss Final con resistencia recibió daño! Vidas: {self.lives}")
                return True
            else:
                print(f"🛡️ ¡ATAQUE COMPLETAMENTE BLOQUEADO!")
                return False
        else:
            # Sin resistencia: aún así más resistente que otros bosses
            import random
            if random.random() < 0.7:  # 70% de probabilidad de hacer daño (no siempre)
                self.lives -= 1
                print(f"💥 Boss Final recibió daño. Vidas: {self.lives}")
                return True
            else:
                print(f"🛡️ Boss Final esquivó el ataque!")
                return False

    def get_bullets(self):
        """Devuelve las balas del boss para manejo externo"""
        return self.bullets

    def clear_bullets(self):
        """Limpia todas las balas del boss"""
        self.bullets = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        # Dibujar balas del boss
        for bullet in self.bullets:
            bullet.draw(surface)
        
        # Dibujar efecto de resistencia
        if self.resistance_active:
            # Efecto de brillo/aura dorada alrededor del boss
            glow_size = 15
            glow_color = (255, 215, 0, 120)  # Dorado semi-transparente
            
            # Crear superficie temporal para el efecto
            glow_surface = pygame.Surface((self.rect.width + glow_size*2, self.rect.height + glow_size*2), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect(), glow_size)
            
            surface.blit(glow_surface, (self.rect.x - glow_size, self.rect.y - glow_size))
        
        # Dibujar barra de vida del boss usando el sistema mejorado
        if self.lives > 0:
            bar_width = 300  # Más ancho para el boss final
            bar_height = 30  # Más alto
            bar_x = surface.get_width() // 2 - bar_width // 2
            bar_y = 30
            
            # Fondo de la barra (más oscuro)
            pygame.draw.rect(surface, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Barra de vida actual con gradiente
            current_width = int((self.lives / self.max_lives) * bar_width)
            # Color que cambia según la vida restante y estado de resistencia
            health_ratio = self.lives / self.max_lives
            if self.resistance_active:
                # Barra dorada brillante cuando tiene resistencia
                color = (255, 215, 0)  # Dorado
                # Efecto de pulso
                pulse = int(50 * (1 + 0.3 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() * 0.3).x))
                color = (min(255, 255), min(255, 215 + pulse), min(255, 0 + pulse))
            elif health_ratio > 0.7:
                color = (255, 0, 0)  # Rojo
            elif health_ratio > 0.3:
                color = (255, 165, 0)  # Naranja
            else:
                color = (255, 255, 0)  # Amarillo (crítico)
            
            pygame.draw.rect(surface, color, (bar_x, bar_y, current_width, bar_height))
            
            # Borde brillante dorado para el boss final
            pygame.draw.rect(surface, (255, 215, 0), (bar_x, bar_y, bar_width, bar_height), 4)
            
            # Texto del boss final
            font = pygame.font.Font(None, 36)
            text = font.render("⚔️ BOSS FINAL - NIVEL 4 ⚔️", True, (255, 215, 0))
            text_rect = text.get_rect(center=(surface.get_width() // 2, bar_y - 30))
            surface.blit(text, text_rect)
            
            # Mostrar vidas numéricamente
            lives_text = font.render(f"{self.lives}/{self.max_lives}", True, (255, 215, 0))
            lives_rect = lives_text.get_rect(center=(surface.get_width() // 2, bar_y + bar_height + 20))
            surface.blit(lives_text, lives_rect) 