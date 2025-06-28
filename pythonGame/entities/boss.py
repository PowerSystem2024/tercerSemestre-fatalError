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
        
        # Comportamiento inteligente mejorado
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
        super().__init__(level, map_size, pos)
        # Boss del nivel 3 es más fuerte
        self.lives = 10  # Más vidas
        self.max_lives = 10
        self.base_speed = self.speed * 0.8  # Velocidad base más lenta
        self.speed = self.base_speed
        
        # Sistema de ataques sorpresivos
        self.dash_cooldown_min = 4.0  # Mínimo 4 segundos
        self.dash_cooldown_max = 8.0  # Máximo 8 segundos
        self.current_dash_cooldown = self.get_random_cooldown()
        self.last_dash_time = 0
        self.dashing = False
        self.dash_duration = 0.8  # Dash dura 0.8 segundos
        self.dash_timer = 0
        self.dash_speed = self.base_speed * 3.5  # 3.5x más rápido durante dash
        
        # Patrón de movimiento táctico
        self.movement_timer = 0
        self.movement_phase = 0  # 0: lento, 1: dash
    
    def get_random_cooldown(self):
        """Genera un cooldown aleatorio para el dash"""
        import random
        return random.uniform(self.dash_cooldown_min, self.dash_cooldown_max)
        
    def update(self, player):
        # Llamar al update básico del Boss (sin el poder especial)
        Enemy.update(self, player)
        
        current_time = pygame.time.get_ticks() / 1000.0
        self.movement_timer += 1/60.0
        
        # Sistema de dash sorpresivo
        if not self.dashing and current_time - self.last_dash_time >= self.current_dash_cooldown:
            # Verificar si el jugador está en rango para dash
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            
            if 200 < distance < 400:  # Solo dash si está a distancia media
                self.start_dash(player)
                self.last_dash_time = current_time
                self.current_dash_cooldown = self.get_random_cooldown()  # Nuevo cooldown aleatorio
        
        if self.dashing:
            self.execute_dash()
        else:
            # Movimiento táctico lento
            self.tactical_movement(player)
    
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
        # Llamar al draw del Boss padre
        super().draw(surface)
        
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
        self.lives = 12  # Aún más vidas porque es el boss final
        self.max_lives = 12  # Para la barra de vida
        self.direction = 'down'
        
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
            # Color que cambia según la vida restante
            health_ratio = self.lives / self.max_lives
            if health_ratio > 0.7:
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