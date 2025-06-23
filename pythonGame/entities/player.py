import pygame
from utils.spritesheet import SpriteSheet
import math
from entities.bullet import Bullet

class Player:
    def __init__(self):
        self.spritesheet = SpriteSheet('assets/jugador/player.png', 'assets/jugador/player.plist', scale=0.15)
        # Animaciones: asumo 4 direcciones, 4 frames cada una (ajustar si es necesario)
        self.animations = {
            'idle': [self.spritesheet.get_image(0)],                # 1.png
            'right': [self.spritesheet.get_image(1), self.spritesheet.get_image(2)],  # 2.png, 3.png
            'left': [self.spritesheet.get_image(3), self.spritesheet.get_image(4)],   # 4.png, 5.png
            'up': [self.spritesheet.get_image(5), self.spritesheet.get_image(6)],     # 6.png, 7.png
            'down': [self.spritesheet.get_image(7), self.spritesheet.get_image(8)]    # 8.png, 9.png
        }
        self.direction = 'down'
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.2
        self.image = self.animations[self.direction][self.anim_index]
        self.rect = self.image.get_rect(center=(960, 540))
        self.speed = 6
        self.lives = 3
        self.last_shot = 0
        self.shoot_delay = 200  # ms

    def handle_event(self, event, bullets):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                mx, my = pygame.mouse.get_pos()
                bullet = Bullet(self.rect.centerx, self.rect.centery, mx, my)
                bullets.append(bullet)
                self.last_shot = now

    def update(self, map_size):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = 'up'
        elif keys[pygame.K_s]:
            dy = self.speed
            self.direction = 'down'
        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = 'left'
        elif keys[pygame.K_d]:
            dx = self.speed
            self.direction = 'right'
        self.rect.x += dx
        self.rect.y += dy
        # Limitar a los bordes del mapa
        self.rect.left = max(0, self.rect.left)
        self.rect.top = max(0, self.rect.top)
        self.rect.right = min(map_size[0], self.rect.right)
        self.rect.bottom = min(map_size[1], self.rect.bottom)
        # Animación
        if dx != 0 or dy != 0:
            self.anim_timer += self.anim_speed
            if self.anim_timer >= 1:
                self.anim_index = (self.anim_index + 1) % len(self.animations[self.direction])
                self.anim_timer = 0
            self.image = self.animations[self.direction][self.anim_index]
        else:
            # Idle: siempre mostrar el frame 0, invertido si la última dirección fue izquierda
            idle_img = self.animations['idle'][0]
            if self.direction == 'left':
                self.image = pygame.transform.flip(idle_img, True, False)
            else:
                self.image = idle_img
            self.anim_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_lives(self, surface):
        for i in range(self.lives):
            pygame.draw.ellipse(surface, (255,0,0), (10 + i*40, 10, 30, 30))

    def hit(self):
        self.lives -= 1

    def reset_position(self, map_size):
        self.rect.center = (map_size[0]//2, map_size[1]//2)

from entities.bullet import Bullet 