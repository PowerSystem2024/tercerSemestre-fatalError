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
        self.spritesheet = SpriteSheet('assets/enemigos/nenemigos3.png', 'assets/enemigos/nenemigos3.plist', scale=1.5)
        # Animaciones usando los nombres específicos del plist
        self.animations = {
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
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.15  # Velocidad de animación un poco más lenta para que se vea mejor
        self.image = self.animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.x = random.randint(0, map_size[0]-self.rect.width)
            self.rect.y = random.randint(0, map_size[1]-self.rect.height)
        self.speed = 2.0 + (level * 0.3)  # Velocidad un poco más rápida para nivel 3

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