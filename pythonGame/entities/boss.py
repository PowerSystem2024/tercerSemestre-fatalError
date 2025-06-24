import pygame
from entities.enemy import Enemy
from utils.spritesheet import SpriteSheet

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
        self.speed = 2 + (level * 0.5)
        self.lives = 4  # Reducimos las vidas del jefe de 5 a 4 