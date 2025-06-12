import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.atan2(target_y - y, target_x - x)
        self.speed = 15
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        if self.rect.bottom < 0:
            del self

    def draw(self, surface):
        surface.blit(self.image, self.rect) 