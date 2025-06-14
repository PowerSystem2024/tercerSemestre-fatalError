import pygame
from entities.enemy import Enemy
from utils.spritesheet import SpriteSheet

class Boss(Enemy):
    def init(self, level, map_size, pos=None):
        super().init(level, map_size, pos)
        self.spritesheet = SpriteSheet('assets/enemigos/enemigos2.png', 'assets/enemigos/enemigos2.plist', scale=0.8)
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
        self.speed = 2 + level
        self.lives = 5  # El jefe tiene más vidas