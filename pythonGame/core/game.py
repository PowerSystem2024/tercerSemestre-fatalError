import pygame
from screens.level_transition import show_level_transition
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
import random
from niveles import nivel1, nivel2, nivel3, nivel4

WINDOW_SIZE = (1280, 720)
MAP_SIZE = (1920, 1080)

class Game:
    def __init__(self, user):
        self.user = user
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Top Down Shooter")
        self.clock = pygame.time.Clock()
        self.level = 1
        self.max_level = 4
        self.enemies_killed = 0
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.running = True
        self.fullscreen = False
        self.background = pygame.image.load('assets/mapa/background1.png').convert()
        self.background = pygame.transform.scale(self.background, MAP_SIZE)
        self.cursor_img = pygame.image.load('assets/cursor/cursor.png').convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (40, 40))
        pygame.mouse.set_visible(False)
        self.sangre_img = pygame.image.load('assets/muerte/sangre.png').convert_alpha()
        self.sangre_img = pygame.transform.scale(self.sangre_img, (60, 60))
        self.sangre_list = []
        self.cargar_nivel()

    def cargar_nivel(self):
        if self.level == 1:
            nivel1.cargar_nivel(self)
        elif self.level == 2:
            nivel2.cargar_nivel(self)
        elif self.level == 3:
            nivel3.cargar_nivel(self)
        elif self.level == 4:
            nivel4.cargar_nivel(self)

    def spawn_enemy_far_from_player(self):
        while True:
            enemy = Enemy(self.level, MAP_SIZE)
            dist = ((enemy.rect.centerx - self.player.rect.centerx) ** 2 + (enemy.rect.centery - self.player.rect.centery) ** 2) ** 0.5
            if dist > 400:
                return enemy

    def next_level(self):
        self.level += 1
        self.enemies_killed = 0
        show_level_transition(self.screen, self.level)
        self.cargar_nivel()
        self.player.reset_position(MAP_SIZE)
        self.sangre_list = []

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)

    def run(self):
        show_level_transition(self.screen, self.level)
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                self.player.handle_event(event, self.bullets)
            self.update()
            self.draw()
            if self.player.lives <= 0:
                from screens.game_over import show_game_over
                restart = show_game_over(self.screen)
                if restart:
                    self.__init__(self.user)
                    show_level_transition(self.screen, self.level)
                else:
                    self.running = False
            if self.enemies_killed >= 10:
                if self.level < self.max_level:
                    self.next_level()
                else:
                    from screens.game_over import show_victory
                    show_victory(self.screen)
                    self.running = False

    def update(self):
        self.player.update(MAP_SIZE)
        for bullet in self.bullets[:]:
            bullet.update()
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.sangre_list.append((enemy.rect.centerx-30, enemy.rect.centery-30))
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.enemies_killed += 1
                    break
        for enemy in self.enemies:
            enemy.update(self.player)
            if enemy.rect.colliderect(self.player.rect):
                self.player.hit()
                self.enemies.remove(enemy)
        while len(self.enemies) < (5 + self.level*2):
            self.enemies.append(self.spawn_enemy_far_from_player())

    def draw(self):
        cam_x = max(0, min(self.player.rect.centerx - WINDOW_SIZE[0]//2, MAP_SIZE[0] - WINDOW_SIZE[0]))
        cam_y = max(0, min(self.player.rect.centery - WINDOW_SIZE[1]//2, MAP_SIZE[1] - WINDOW_SIZE[1]))
        camera = pygame.Rect(cam_x, cam_y, WINDOW_SIZE[0], WINDOW_SIZE[1])
        map_surface = self.background.copy()
        for pos in self.sangre_list:
            map_surface.blit(self.sangre_img, pos)
        self.player.draw(map_surface)
        for enemy in self.enemies:
            enemy.draw(map_surface)
        for bullet in self.bullets:
            bullet.draw(map_surface)
        self.player.draw_lives(map_surface)
        self.screen.blit(map_surface, (0,0), camera)
        mx, my = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, (mx-20, my-20))
        pygame.display.flip() 