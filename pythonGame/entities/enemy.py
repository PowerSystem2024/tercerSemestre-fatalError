import pygame
import random
from utils.spritesheet import SpriteSheet
import math

class Enemy:
    def __init__(self, level, map_size, pos=None):
        self.spritesheet = SpriteSheet('assets/enemigos/enemigoslevel1.png', 'assets/enemigos/enemigoslevel1.plist', scale=0.5)
        # Animaciones: asumo 4 direcciones, 4 frames cada una (ajustar si es necesario)
        self.animations = {
            'down': self.spritesheet.get_images_by_range(0, 4),
            'left': self.spritesheet.get_images_by_range(4, 8),
            'right': self.spritesheet.get_images_by_range(8, 12),
            'up': self.spritesheet.get_images_by_range(12, 16)
        }
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.12
        self.image = self.animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.x = random.randint(0, map_size[0]-self.rect.width)
            self.rect.y = random.randint(0, map_size[1]-self.rect.height)
        self.speed = 1.5 + (level * 0.5)

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        self.rect.x += int(self.speed * dx / dist)
        self.rect.y += int(self.speed * dy / dist)
        # Dirección para animación
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'
        # Animación
        self.anim_timer += self.anim_speed
        if self.anim_timer >= 1:
            self.anim_index = (self.anim_index + 1) % len(self.animations[self.direction])
            self.anim_timer = 0
        self.image = self.animations[self.direction][self.anim_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy2:
    def __init__(self, level, map_size, pos=None):
        self.spritesheet = SpriteSheet('assets/enemigos/enemigos2.png', 'assets/enemigos/enemigos2.plist', scale=0.5)
        self.animations = {
            'down': self.spritesheet.get_images_by_range(0, 4),
            'left': self.spritesheet.get_images_by_range(4, 8),
            'right': self.spritesheet.get_images_by_range(8, 12),
            'up': self.spritesheet.get_images_by_range(12, 16)
        }
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.12
        self.image = self.animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.x = random.randint(0, map_size[0]-self.rect.width)
            self.rect.y = random.randint(0, map_size[1]-self.rect.height)
        self.speed = 1.5 + (level * 0.5)

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        self.rect.x += int(self.speed * dx / dist)
        self.rect.y += int(self.speed * dy / dist)
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'
        self.anim_timer += self.anim_speed
        if self.anim_timer >= 1:
            self.anim_index = (self.anim_index + 1) % len(self.animations[self.direction])
            self.anim_timer = 0
        self.image = self.animations[self.direction][self.anim_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy3:
    def __init__(self, level, map_size, pos=None):
        # Spritesheet para movimiento normal
        self.spritesheet = SpriteSheet('assets/enemigos/nenemigos3.png', 'assets/enemigos/nenemigos3.plist', scale=1.5)
        # Spritesheet para ataques
        self.attack_spritesheet = SpriteSheet('assets/enemigos/ataques/ataque-enemigo-3.png', 'assets/enemigos/ataques/ataque-enemigo-3.plist', scale=1.5)
        
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
        
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.15  # Velocidad de animación un poco más lenta para que se vea mejor
        self.image = self.move_animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.x = random.randint(0, map_size[0]-self.rect.width)
            self.rect.y = random.randint(0, map_size[1]-self.rect.height)
        self.speed = 2.0 + (level * 0.3)  # Velocidad un poco más rápida para nivel 3
        
        # Variables para el ataque
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 1.0  # Duración del ataque en segundos
        self.attack_cooldown = 1.5  # Tiempo entre ataques en segundos (reducido)
        self.last_attack_time = 0
        self.attack_range = 100  # Distancia a la que puede atacar (aumentado)
        self.attack_damage = 1  # Daño que hace al jugador
        
        # Cargar sonido de ataque si existe
        try:
            self.attack_sound = pygame.mixer.Sound('sonidos/BichosNoise.wav')
        except:
            self.attack_sound = None
            
        # Debug: Verificar que las animaciones se cargaron correctamente (comentado para producción)
        # print(f"Enemy3 inicializado:")
        # print(f"  - Animaciones de movimiento: {len(self.move_animations['down'])} frames")
        # print(f"  - Animaciones de ataque: {len(self.attack_animations['down'])} frames")
        # print(f"  - Rango de ataque: {self.attack_range}")
        # print(f"  - Cooldown: {self.attack_cooldown}")
        
        # Verificar que los sprites de ataque no sean None
        for direction in ['down', 'left', 'right', 'up']:
            for i, sprite in enumerate(self.attack_animations[direction]):
                if sprite is None:
                    print(f"ERROR: Sprite de ataque {direction}[{i}] es None")

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        
        current_time = pygame.time.get_ticks() / 1000.0  # Convertir a segundos
        
        # Actualizar dirección basada en la posición del jugador
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'
        
        # Si está atacando, actualizar animación de ataque
        if self.is_attacking:
            self.attack_timer += 1/60.0  # Asumiendo 60 FPS
            
            # Animación de ataque
            self.anim_timer += self.anim_speed * 2.0  # Ataque más rápido
            if self.anim_timer >= 1:
                self.anim_index = (self.anim_index + 1) % len(self.attack_animations[self.direction])
                self.anim_timer = 0
                
                # Verificar daño en el frame de impacto
                if self.anim_index == 2:
                    attack_rect = self.get_attack_rect()
                    if attack_rect.colliderect(player.hitbox):
                        hit_successful = player.hit()
                        # if hit_successful:
                        #     print("¡Enemigo golpeó al jugador!")
            
            self.image = self.attack_animations[self.direction][self.anim_index]
            
            # Terminar ataque
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
                self.anim_index = 0
        else:
            # Verificar si puede atacar
            can_attack = (dist <= self.attack_range and 
                         current_time - self.last_attack_time >= self.attack_cooldown)
            
            if can_attack:
                # Iniciar ataque
                self.is_attacking = True
                self.attack_timer = 0
                self.last_attack_time = current_time
                self.anim_index = 0
                self.anim_timer = 0
                if self.attack_sound:
                    self.attack_sound.play()
            else:
                # Movimiento normal hacia el jugador
                self.rect.x += int(self.speed * dx / dist)
                self.rect.y += int(self.speed * dy / dist)
                
                # Animación de movimiento
                self.anim_timer += self.anim_speed
                if self.anim_timer >= 1:
                    self.anim_index = (self.anim_index + 1) % len(self.move_animations[self.direction])
                    self.anim_timer = 0
                self.image = self.move_animations[self.direction][self.anim_index]

    def get_attack_rect(self):
        """Obtiene el rectángulo de ataque basado en la dirección"""
        attack_rect = self.rect.copy()
        
        if self.direction == 'right':
            attack_rect.x += self.rect.width
            attack_rect.width = 40
        elif self.direction == 'left':
            attack_rect.x -= 40
            attack_rect.width = 40
        elif self.direction == 'down':
            attack_rect.y += self.rect.height
            attack_rect.height = 40
        elif self.direction == 'up':
            attack_rect.y -= 40
            attack_rect.height = 40
            
        return attack_rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        # Debug: Dibujar el área de ataque y estado (comentado para producción)
        # if self.is_attacking:
        #     attack_rect = self.get_attack_rect()
        #     pygame.draw.rect(surface, (255, 0, 0), attack_rect, 3)
        #     # Mostrar texto de debug
        #     font = pygame.font.Font(None, 24)
        #     text = font.render("ATTACKING!", True, (255, 0, 0))
        #     surface.blit(text, (self.rect.x, self.rect.y - 25))
        
        # Dibujar círculo de rango de ataque (comentado para producción)
        # pygame.draw.circle(surface, (255, 255, 0), self.rect.center, self.attack_range, 1)

from entities.bullet import Bullet, EnemyBullet

class Enemy4:
    def __init__(self, level, map_size, pos=None):
        # Usar sprites de enemigos normales para movimiento (misma escala que Enemy1)
        self.spritesheet = SpriteSheet('assets/enemigos/enemigoslevel1.png', 'assets/enemigos/enemigoslevel1.plist', scale=0.5)
        # Spritesheet para ataques a distancia (escala ajustada para que se vea bien)
        self.attack_spritesheet = SpriteSheet('assets/enemigos/ataques/ataque-enemigo-4.png', 'assets/enemigos/ataques/ataque-enemigo-4.plist', scale=0.7)
        
        # Animaciones de movimiento
        self.move_animations = {
            'down': self.spritesheet.get_images_by_range(0, 4),
            'left': self.spritesheet.get_images_by_range(4, 8),
            'right': self.spritesheet.get_images_by_range(8, 12),
            'up': self.spritesheet.get_images_by_range(12, 16)
        }
        
        # Animaciones de ataque (disparos)
        self.attack_animations = {
            'down': [
                self.attack_spritesheet.get_image_by_name('ataqueAbajo1.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueAbajo2.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueAbajo3.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueAbajo4.png')
            ],
            'left': [
                self.attack_spritesheet.get_image_by_name('AtaqueIzquierda1.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueIzquierda2.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueIzquierda3.png'),
                self.attack_spritesheet.get_image_by_name('ataqueIzquierda4.png')
            ],
            'right': [
                self.attack_spritesheet.get_image_by_name('AtaqueDerecha1.png'),
                self.attack_spritesheet.get_image_by_name('ataqueDerecha2.png'),
                self.attack_spritesheet.get_image_by_name('ataqueDerecha3.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueDerecha4.png')
            ],
            'up': [
                self.attack_spritesheet.get_image_by_name('AtaqueArriba1.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueArriba2.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueArriba3.png'),
                self.attack_spritesheet.get_image_by_name('AtaqueArriba4.png')
            ]
        }
        
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.12
        self.image = self.move_animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.x = random.randint(0, map_size[0]-self.rect.width)
            self.rect.y = random.randint(0, map_size[1]-self.rect.height)
        self.speed = 1.8 + (level * 0.2)  # Velocidad moderada
        
        # Variables para el ataque a distancia
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.8  # Duración del ataque en segundos
        self.attack_cooldown = 2.5  # Tiempo entre ataques en segundos
        self.last_attack_time = 0
        self.attack_range = 250  # Rango de disparo más largo
        self.bullets = []  # Lista de balas del enemigo
        
        # Cargar sonido de disparo si existe
        try:
            self.shoot_sound = pygame.mixer.Sound('sonidos/Disparo.wav')
        except:
            self.shoot_sound = None
            
        # Verificar que los sprites de ataque se cargaron
        for direction in ['down', 'left', 'right', 'up']:
            for i, sprite in enumerate(self.attack_animations[direction]):
                if sprite is None:
                    print(f"ERROR: Sprite de ataque Enemy4 {direction}[{i}] es None")

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        
        current_time = pygame.time.get_ticks() / 1000.0  # Convertir a segundos
        
        # Actualizar dirección basada en la posición del jugador
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'
        
        # Actualizar balas del enemigo
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]
        
        # Si está atacando, actualizar animación de ataque
        if self.is_attacking:
            self.attack_timer += 1/60.0  # Asumiendo 60 FPS
            
            # Animación de ataque
            self.anim_timer += self.anim_speed * 2.5  # Ataque más rápido
            if self.anim_timer >= 1:
                self.anim_index = (self.anim_index + 1) % len(self.attack_animations[self.direction])
                self.anim_timer = 0
                
                # Disparar en el frame de disparo
                if self.anim_index == 2:  # Frame de disparo
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, 
                                       player.rect.centerx, player.rect.centery)
                    self.bullets.append(bullet)
                    if self.shoot_sound:
                        self.shoot_sound.play()
            
            self.image = self.attack_animations[self.direction][self.anim_index]
            
            # Terminar ataque
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
                self.anim_index = 0
        else:
            # Verificar si puede atacar
            can_attack = (dist <= self.attack_range and 
                         current_time - self.last_attack_time >= self.attack_cooldown)
            
            if can_attack:
                # Iniciar ataque
                self.is_attacking = True
                self.attack_timer = 0
                self.last_attack_time = current_time
                self.anim_index = 0
                self.anim_timer = 0
            else:
                # Movimiento: mantener distancia óptima para disparar
                if dist > self.attack_range:
                    # Acercarse si está muy lejos
                    self.rect.x += int(self.speed * dx / dist)
                    self.rect.y += int(self.speed * dy / dist)
                elif dist < self.attack_range * 0.7:
                    # Alejarse si está muy cerca
                    self.rect.x -= int(self.speed * dx / dist * 0.5)
                    self.rect.y -= int(self.speed * dy / dist * 0.5)
                # Si está en rango óptimo, no moverse
                
                # Animación de movimiento
                if dist > self.attack_range or dist < self.attack_range * 0.7:
                    self.anim_timer += self.anim_speed
                    if self.anim_timer >= 1:
                        self.anim_index = (self.anim_index + 1) % len(self.move_animations[self.direction])
                        self.anim_timer = 0
                    self.image = self.move_animations[self.direction][self.anim_index]

    def get_bullets(self):
        """Devuelve las balas del enemigo para manejo externo"""
        return self.bullets

    def clear_bullets(self):
        """Limpia todas las balas del enemigo"""
        self.bullets = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        # Dibujar balas del enemigo
        for bullet in self.bullets:
            bullet.draw(surface)
        
        # Debug: Dibujar rango de ataque (comentado para producción)
        # pygame.draw.circle(surface, (255, 0, 255), self.rect.center, self.attack_range, 1) 