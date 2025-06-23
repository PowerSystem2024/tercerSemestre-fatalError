# entities/smart_enemy.py

import pygame
from pygame.math import Vector2

class SmartEnemy:
    def __init__(self, player):
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Rojo
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)  # Posición inicial
        self.speed = 2
        self.player = player

    def update(self, player):
        # Movimiento básico hacia el jugador
        direction = Vector2(player.rect.center) - Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
