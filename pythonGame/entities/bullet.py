import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        # Cargar imagen del proyectil del jugador
        try:
            self.original_image = pygame.image.load('assets/enemigos/balas/disparoPlayer1.png').convert_alpha()
            # Escalar la imagen del proyectil
            self.original_image = pygame.transform.scale(self.original_image, (50, 30))
            print("✅ Imagen disparoPlayer1.png cargada correctamente")
        except Exception as e:
            # Fallback: crear bala simple si no encuentra la imagen
            self.original_image = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (255, 255, 0), (5, 5), 5)
            print(f"❌ No se pudo cargar disparoPlayer1.png: {e}")
        
        # Calcular ángulo y dirección
        angle = math.atan2(target_y - y, target_x - x)
        self.speed = 15
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
        # Rotar la imagen para que apunte hacia el objetivo
        # Asumiendo que la imagen original apunta hacia la derecha
        angle_degrees = math.degrees(angle)
        self.image = pygame.transform.rotate(self.original_image, -angle_degrees)
        
        # Centrar el rect después de la rotación
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        if self.rect.bottom < 0:
            del self

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class EnemyBullet:
    def __init__(self, x, y, target_x, target_y):
        # Cargar imagen del proyectil enemigo
        try:
            self.original_image = pygame.image.load('assets/enemigos/balas/disparoEnemigo4.png').convert_alpha()
            # Escalar la imagen del proyectil
            self.original_image = pygame.transform.scale(self.original_image, (25, 15))
            print("✅ Imagen disparoEnemigo4.png cargada correctamente")
        except Exception as e:
            # Fallback: crear bala simple si no encuentra la imagen
            self.original_image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (255, 100, 100), (6, 6), 6)
            pygame.draw.circle(self.original_image, (255, 0, 0), (6, 6), 4)
            print(f"❌ No se pudo cargar disparoEnemigo4.png: {e}")
        
        # Calcular ángulo y dirección
        angle = math.atan2(target_y - y, target_x - x)
        self.speed = 8  # Más lenta que las balas del jugador
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.lifetime = 180  # 3 segundos a 60 FPS
        
        # Rotar la imagen para que apunte hacia el objetivo
        # La imagen original apunta hacia la izquierda, así que ajustamos
        angle_degrees = math.degrees(angle)
        # Ajustar para que la imagen apunte correctamente
        rotation_angle = angle_degrees + 180  # +180 porque la imagen apunta a la izquierda
        self.image = pygame.transform.rotate(self.original_image, -rotation_angle)
        
        # Centrar el rect después de la rotación
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        self.lifetime -= 1
        
        # Eliminar si sale del mapa o se acaba el tiempo
        if (self.rect.right < 0 or self.rect.left > 1920 or 
            self.rect.bottom < 0 or self.rect.top > 1080 or 
            self.lifetime <= 0):
            return False  # Indica que debe ser eliminada
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect) 