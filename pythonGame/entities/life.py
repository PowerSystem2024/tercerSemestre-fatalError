import pygame

class Life:
    def __init__(self, x, y):
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255,40,40), (0, 0, 26, 26))  # Corazón rojo simple
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect) 