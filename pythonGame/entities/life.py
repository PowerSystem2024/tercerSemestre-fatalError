import pygame

class Life:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/corazon/VIDA1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Escalar al mismo tamaño
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect) 