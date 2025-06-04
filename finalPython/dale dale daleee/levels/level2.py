import pygame
import random
from itertools import repeat
import math


#inicializamos pygame
pygame.init()
pygame.font.get_init()


# CONSTANTES:


#modo debug 
IS_DEBUG = True  # Activamos el modo debug para mostrar las hitboxes

#colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#configuracion de ventana 
WINDOW_SIZE = (1280, 720)
WINDOW_TITLE = "Dale dale daleeee"
FRAME_RATE = 60

#limites 
BOUNDS_X = (66, 1214)
BOUNDS_Y = (50, 620)
#direcciones de animaciones 
DOWN, HORIZONTAL, UP = 0, 1, 2

#tamaño de los objetos
PLAYER_SIZE = (72, 72)
ENEMY_SIZE = (72, 72)  # Aumentamos el tamaño del enemigo para mejor visualización
PARTICLES_SIZE = (72, 72)
BULLET_SIZE = (16, 16)

#config del cursor 
CURSOR_MIN_SIZE = 50
CURSOR_INCREASE_EFFECT = 25
CURSOR_SHRINK_SPEED = 3

#rutas de recursos 
BACKGROUND = "../assets/background1.png"
PLAYER_TILESET = "../assets/player-Sheet.png"
ENEMY_TILESET = "../assets/enemy-Sheet.png"
BULLET = "../assets/bullet.png"
CURSOR = "../assets/cursor.png"
HEART_FULL = "../assets/heart.png"
HEART_EMPTY = "../assets/heart_empty.png"
PARTICLES = "../assets/particles.png"

#texto en la interfaz
START_GAME_TEXT = "Espacio para empezar"
GAME_OVER_TEXT = "Perdiste:C, R para reiniciar"

# config de balance del juego
DIFFICULTY = 1.5  # Aumentamos la dificultad base
PLAYER_MAX_HEALTH = 3
PLAYER_SPEED = 4
ENEMY_MAX_HEALTH = 3
ENEMY_SPEED = 2.5  # Aumentamos la velocidad base de los enemigos
ENEMY_DASH_SPEED = 5  # Velocidad de dash
ENEMY_DASH_COOLDOWN = 180  # Frames entre cada dash (3 segundos)
BULLET_SPEED = 10
ENEMY_SPAWN_DISTANCE = 250
BULLETS_RICOCHET = False
HEART_DROP_FREQUENCY = 15  # Cada cuántos enemigos aparece un corazón
HEART_SIZE = (32, 32)  # Tamaño del corazón en pantalla

# Configuración del jefe
BOSS_SIZE = (144, 144)  # El doble del tamaño normal
BOSS_HEALTH = 30
BOSS_SPEED = 2
BOSS_DASH_SPEED = 8
BOSS_SCORE_THRESHOLD = 25  # Puntaje necesario para que aparezca el jefe

# Variables globales del juego
score = 0
high_score = 0
has_game_started = False
is_game_over = False



#CONFIGURACION PARA PYGAME 


# config de pantalla con soporte de temblor 
SHAKE_WINDOW = pygame.display.set_mode(WINDOW_SIZE)
WINDOW = SHAKE_WINDOW.copy()
clock = pygame.time.Clock()

#fuente
text_font = pygame.font.Font("../assets/font.otf", 32)

#contenedores globales
#objetos dibujables 
objects = [] 
#desplazamiento para temblor de pantalla 
offset = repeat((0, 0))

# Inicializar target global
target = None



#CLASES BASE


class Object:
    #clase base para todos los objetos del juego 
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = None if image is None else pygame.image.load(image).convert_alpha()
        self.collider = [width, height] #tamaño de caja de colision 
        self.velocity = [0, 0] #velocidad de movimiento
        objects.append(self)

    def draw(self):
        #dibujar el objeto en pantalla
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y)) 

    def update(self):
        #actualiza posicion y dibuja el objeto 
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        #obtener coordenadas dentro del objeto 
        return self.x + self.width / 2, self.y + self.height / 2


class Entity(Object):
    #entinity es la entidad que es jugador/enemigo 
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, None)
        self.speed = speed

        #animacion 
        self.tileset = load_tileset(tileset, 16, 16)  # Mantenemos 16x16 como base
        self.direction = DOWN #direccion actual 
        self.flipX = False #forma horizontal 
        self.frame = 0 #frame actual de animacion
        self.frames = [0, 1, 2, 1] #secuencia para que se vea el movimiento 
        self.frame_timer = 0 #temporizador para velocidad de animacion 
        self.is_moving = False

    def change_direction(self):
        #actualizamos direcciones del sprite depende de la velocidad 
        old_direction = self.direction
        old_flip = self.flipX
        
        if abs(self.velocity[0]) > abs(self.velocity[1]):
            self.direction = HORIZONTAL
            self.flipX = self.velocity[0] < 0
            self.is_moving = self.velocity[0] != 0
        else:
            if self.velocity[1] > 0:
                self.direction = DOWN
                self.is_moving = True
            elif self.velocity[1] < 0:
                self.direction = UP
                self.is_moving = True
            else:
                self.is_moving = False

        # Si cambiamos de dirección, reiniciamos el frame
        if old_direction != self.direction or old_flip != self.flipX:
            self.frame = 0
            self.frame_timer = 0

    def draw(self):
        if not hasattr(self, 'tileset') or not self.tileset:
            return
            
        try:
            # Actualizamos la dirección antes de dibujar
            self.change_direction()
            
            # Asegurarnos que tenemos frames válidos
            if len(self.tileset) > self.direction and len(self.tileset[self.direction]) > self.frames[self.frame]:
                img = self.tileset[self.direction][self.frames[self.frame]]
                
                # Escalamos al tamaño actual
                img = pygame.transform.scale(img, (self.width, self.height))
                
                # Aplicamos flip si es necesario
                if self.flipX:
                    img = pygame.transform.flip(img, True, False)
                
                # Dibujamos en la posición
                WINDOW.blit(img, (self.x, self.y))
                
                # Debug: mostrar collider
                if IS_DEBUG:
                    x, y = self.get_center()
                    pygame.draw.rect(WINDOW, RED, 
                                   (x - self.collider[0] / 2, 
                                    y - self.collider[1] / 2, 
                                    self.collider[0], 
                                    self.collider[1]), width=1)
            else:
                print(f"Frame inválido: direction={self.direction}, frame={self.frames[self.frame]}")
                print(f"Tamaños: tileset rows={len(self.tileset)}, cols={len(self.tileset[0]) if self.tileset else 0}")
        except Exception as e:
            print(f"Error al dibujar sprite: {e}")
            return

        # Actualización de animación solo si nos estamos moviendo
        if not self.is_moving:
            self.frame = 0
            return

        self.frame_timer += 1
        if self.frame_timer < 15:  # Hacemos la animación más lenta y estable
            return

        self.frame = (self.frame + 1) % len(self.frames)
        self.frame_timer = 0




#FUNCIONES UTILITARIAS 


def load_tileset(filename, width, height):
    try:
        # Cargar imagen
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        
        # Verificar dimensiones de la imagen
        print(f"Dimensiones de {filename}: {image_width}x{image_height}")
        
        tileset = []
        rows = image_height // height  # Número de filas (direcciones)
        cols = image_width // width    # Número de columnas (frames)
        
        print(f"Dividiendo en {rows} filas y {cols} columnas")
        
        # Primero por filas (direcciones)
        for row in range(rows):
            line = []
            tileset.append(line)
            # Luego por columnas (frames)
            for col in range(cols):
                rect = (col * width, row * height, width, height)
                if rect[0] + width <= image_width and rect[1] + height <= image_height:
                    tile = image.subsurface(rect)
                    line.append(tile)
                    
        return tileset
    except Exception as e:
        print(f"Error cargando tileset {filename}: {e}")
        # Retornamos un tileset con un sprite en blanco como fallback
        dummy = pygame.Surface((width, height), pygame.SRCALPHA)
        dummy.fill((255, 0, 255))  # Color magenta para identificar errores
        return [[dummy]]



#CLASES DE ENTIDADES DEL JUEGO

class Player(Entity):
    #clase del personaje con el que jugamos
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        self.health = self.max_health = PLAYER_MAX_HEALTH


class Enemy(Entity):
    #clase del enemigo con ia
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        #propiedades de animacion de crecimiento 
        self.m_width = width
        self.m_height = height
        self.width = 0
        self.height = 0
        self.grow_speed = 2

        # Ajustamos el tamaño del collider para mantener la jugabilidad
        self.collider = [width / 3, height / 2]  # Ajustamos el collider para el nuevo tamaño
        
        # Nuevas variables para comportamientos
        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_direction = [0, 0]
        self.original_speed = speed
        self.movement_pattern = random.choice(['perseguir', 'circular', 'zigzag'])
        self.pattern_timer = 0
        self.zigzag_direction = 1

        self.health = ENEMY_MAX_HEALTH
        enemies.append(self)

    def update(self):
        #actualizamos el comportamiento del enemigo 
        #animacion del crecimiento 
        if self.width < self.m_width:
            self.width += self.grow_speed
        if self.height < self.m_height:
            self.height += self.grow_speed

        #ia: se mueve hacia nosotros el enemigo 
        player_center = player.get_center()
        enemy_center = self.get_center()
        #calcular vector de direccion hacia nosotros 
        self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]
        #normalizar y aplicamos velocidad
        length = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        if length > 0:
            self.velocity = [self.velocity[0] / length, self.velocity[1] / length]
            self.velocity = [self.velocity[0] * self.speed, self.velocity[1] * self.speed]

        # Actualizar posición
        new_x = self.x + self.velocity[0]
        new_y = self.y + self.velocity[1]
        
        # Mantener dentro de los límites
        self.x = max(BOUNDS_X[0], min(new_x, BOUNDS_X[1] - self.width))
        self.y = max(BOUNDS_Y[0], min(new_y, BOUNDS_Y[1] - self.height))
        
        super().draw()  # Solo dibujamos, no usamos el update de Entity

    def take_damage(self, damage):
        #manejamos el resibir daño y destruccion
        self.health -= damage
        if self.health > 0:
            return

        #efectos de muerte
        global score, offset
        score += 1
        
        # Verificar si debemos dropear un corazón
        if score % HEART_DROP_FREQUENCY == 0:
            heart = HeartDrop(self.x + self.width/2 - HEART_SIZE[0]/2, 
                            self.y + self.height/2 - HEART_SIZE[1]/2)
            hearts.append(heart)
            # Efecto visual para el corazón
            spawn_particles(heart.x, heart.y)
        
        #tiembla la pantalla
        offset = screen_shake(6, 7)
        #particulas de muerte 
        spawn_particles(self.x, self.y)

        self.destroy()

    def destroy(self):
        #sacar enemigo del jogo 
        objects.remove(self)
        enemies.remove(self)


class Boss(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        # Propiedades base
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.original_speed = speed
        
        # Propiedades de ataque
        self.attack_pattern = 0
        self.attack_timer = 0
        self.is_dashing = False
        self.dash_direction = [0, 0]
        self.dash_cooldown = 0
        
        # Propiedades de animación de crecimiento
        self.m_width = width
        self.m_height = height
        self.width = width
        self.height = height
        self.grow_speed = 4
        
        # Hitboxes más grandes
        self.hitboxes = {
            'cabeza': [width/4, 0, width/2, height/2.5],  # Hitbox más grande para la cabeza
            'cuerpo': [width/6, height/3, width*2/3, height/2],  # Hitbox más ancha para el cuerpo
            'pies': [width/4, height*2/3, width/2, height/3]   # Hitbox más alta para los pies
        }
        
        # Collider general más grande para colisiones con el jugador
        self.collider = [width*0.7, height*0.7]

    def update(self):
        # Animación de crecimiento
        if self.width < self.m_width:
            self.width += self.grow_speed
        if self.height < self.m_height:
            self.height += self.grow_speed

        player_center = player.get_center()
        boss_center = self.get_center()
        
        # Gestión del dash
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
            if self.dash_cooldown == 0:
                self.is_dashing = False
                self.speed = self.original_speed

        # Actualizar timer de ataque
        self.attack_timer += 1
        if self.attack_timer >= 180:  # Cambiar patrón cada 3 segundos
            self.attack_timer = 0
            self.attack_pattern = (self.attack_pattern + 1) % 3
            
            # Iniciar dash al cambiar a patrón 2
            if self.attack_pattern == 2 and not self.is_dashing:
                self.is_dashing = True
                self.dash_cooldown = 60
                self.speed = BOSS_DASH_SPEED
                dx = player_center[0] - boss_center[0]
                dy = player_center[1] - boss_center[1]
                length = (dx ** 2 + dy ** 2) ** 0.5
                if length > 0:
                    self.dash_direction = [dx/length, dy/length]

        # Calcular nueva velocidad según el patrón
        if self.attack_pattern == 0:
            # Patrón 1: Persecución normal
            dx = player_center[0] - boss_center[0]
            dy = player_center[1] - boss_center[1]
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length > 0:
                self.velocity = [dx/length * self.speed, dy/length * self.speed]
        
        elif self.attack_pattern == 1:
            # Patrón 2: Movimiento circular
            angle = self.attack_timer * 0.1
            radius = 200
            target_x = player_center[0] + math.cos(angle) * radius
            target_y = player_center[1] + math.sin(angle) * radius
            dx = target_x - boss_center[0]
            dy = target_y - boss_center[1]
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length > 0:
                self.velocity = [dx/length * self.speed, dy/length * self.speed]
        
        else:
            # Patrón 3: Dash hacia el jugador
            if self.is_dashing:
                self.velocity = [self.dash_direction[0] * self.speed,
                               self.dash_direction[1] * self.speed]
            else:
                self.velocity = [0, 0]

        # Actualizar posición con límites
        new_x = self.x + self.velocity[0]
        new_y = self.y + self.velocity[1]
        
        # Mantener dentro de los límites
        self.x = max(BOUNDS_X[0], min(new_x, BOUNDS_X[1] - self.width))
        self.y = max(BOUNDS_Y[0], min(new_y, BOUNDS_Y[1] - self.height))
        
        self.draw()  # Llamamos a draw en lugar de super().draw()

    def draw(self):
        super().draw()
        
        # Dibujar hitboxes en modo debug con colores diferentes
        if IS_DEBUG:
            colors = {
                'cabeza': (255, 0, 0),  # Rojo para la cabeza
                'cuerpo': (0, 255, 0),  # Verde para el cuerpo
                'pies': (0, 0, 255)     # Azul para los pies
            }
            
            for hitbox_name, hitbox in self.hitboxes.items():
                pygame.draw.rect(WINDOW, colors[hitbox_name],
                               (self.x + hitbox[0],
                                self.y + hitbox[1],
                                hitbox[2],
                                hitbox[3]),
                               width=2)
                
            # Dibujar el collider general
            x, y = self.get_center()
            pygame.draw.rect(WINDOW, (255, 255, 0),  # Amarillo para el collider general
                           (x - self.collider[0]/2,
                            y - self.collider[1]/2,
                            self.collider[0],
                            self.collider[1]),
                           width=2)
        
        try:
            # Dibujar barra de vida del jefe
            health_width = 300  # Barra más ancha
            health_height = 30  # Barra más alta
            health_x = WINDOW_SIZE[0]/2 - health_width/2
            health_y = 20  # Un poco más arriba
            
            # Borde negro más grueso
            pygame.draw.rect(WINDOW, BLACK, 
                            (health_x-4, health_y-4, health_width+8, health_height+8))
            
            # Fondo rojo oscuro
            pygame.draw.rect(WINDOW, (139, 0, 0), 
                            (health_x, health_y, health_width, health_height))
            
            # Vida actual en rojo brillante con degradado
            health_percentage = self.health / self.max_health
            current_health_width = health_width * health_percentage
            
            # Gradiente de color basado en la vida restante
            if health_percentage > 0.6:
                health_color = (0, 255, 0)  # Verde para vida alta
            elif health_percentage > 0.3:
                health_color = (255, 165, 0)  # Naranja para vida media
            else:
                health_color = (255, 0, 0)  # Rojo para vida baja
                
            pygame.draw.rect(WINDOW, health_color, 
                            (health_x, health_y, current_health_width, health_height))
            
            # Texto con la cantidad de vida
            health_text = text_font.render(f"{self.health}/{self.max_health}", True, WHITE)
            text_x = health_x + (health_width - health_text.get_width()) / 2
            text_y = health_y + (health_height - health_text.get_height()) / 2
            WINDOW.blit(health_text, (text_x, text_y))
        except Exception as e:
            print(f"Error al dibujar la barra de vida: {e}")

    def check_hit(self, bullet):
        # Verificar colisión con cada hitbox
        bullet_center = bullet.get_center()
        for hitbox_name, hitbox in self.hitboxes.items():
            hitbox_x = self.x + hitbox[0]
            hitbox_y = self.y + hitbox[1]
            
            if (hitbox_x <= bullet_center[0] <= hitbox_x + hitbox[2] and
                hitbox_y <= bullet_center[1] <= hitbox_y + hitbox[3]):
                # Daño extra si golpea en la cabeza
                damage = 2 if hitbox_name == 'cabeza' else 1
                self.take_damage(damage)
                return True
        return False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            global score
            score += 50  # Bonus de puntuación por derrotar al jefe
            self.destroy()
            return True
        return False

    def destroy(self):
        objects.remove(self)
        global boss
        boss = None
        # Efecto de muerte más dramático
        for _ in range(5):
            spawn_particles(self.x + random.randint(0, self.width),
                          self.y + random.randint(0, self.height))
        offset = screen_shake(10, 15)  # Temblor más fuerte


class HeartDrop(Object):
    def __init__(self, x, y):
        super().__init__(x, y, HEART_SIZE[0], HEART_SIZE[1], HEART_FULL)
        self.collider = [self.width, self.height]
        self.float_offset = 0  # Para el efecto de flotación
        self.float_speed = 0.1  # Velocidad del efecto
        
    def update(self):
        # Efecto de flotación
        self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * 5
        self.draw()
        
    def draw(self):
        # Dibujamos el corazón con efecto de flotación
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), 
                   (self.x, self.y + self.float_offset))
        
        # Debug: mostrar collider
        if IS_DEBUG:
            x, y = self.get_center()
            pygame.draw.rect(WINDOW, RED, 
                           (x - self.collider[0] / 2, 
                            y - self.collider[1] / 2, 
                            self.collider[0], 
                            self.collider[1]), width=1)

# Lista global para los corazones
hearts = []




# OBJETOS GLOBALES DEL JUEGO 


#cursor para apuntar 
global player, bullets
target = Object(100, 100, CURSOR_MIN_SIZE, CURSOR_MIN_SIZE, CURSOR)
#lista de todos los enemigos
enemies = []
#lista de efecto de particulas
particles = []

# Variable global para el jefe
boss = None




# FUNCIONES PRINCIPALES DEL JUEGO


def load_high_score():
    #cargar puntacion maxima desde la base de datos
    global high_score
    # Inicializamos en 0 ya que no usamos base de datos en este nivel
    high_score = 0


def start():
    #inicializar/reinicial el juego 
    global player, bullets, score

    #crear jugador en el medio de la pantalla 
    player = Player(WINDOW_SIZE[0] / 2 - 37.5, WINDOW_SIZE[1] / 2 - 37.5, 75, 75, PLAYER_TILESET, PLAYER_SPEED)
    player.collider = [player.width / 2.5, player.height / 2]

    bullets = []
    score = 0
    load_high_score()


def game_over():
    #manejamos el estado del fin del juego 
    global is_game_over, high_score
    #actualizamos la puntacion maxima si es que la mejoramos
    if score > high_score:
        high_score = score
    is_game_over = True


def shoot():
    #disparar unabala hacia el cursor 
    player_center = player.get_center()
    bullet = Object(player_center[0], player_center[1], BULLET_SIZE[0], BULLET_SIZE[1], BULLET)
    
    #calcular direccion hacia el cursor 
    bullet.velocity = [target.x + target.width / 2 - bullet.x, target.y + target.height / 2 - bullet.y]

    #normalizar y meterle velocidad 
    length = (bullet.velocity[0] ** 2 + bullet.velocity[1] ** 2) ** 0.5
    bullet.velocity = [bullet.velocity[0] / length, bullet.velocity[1] / length]
    bullet.velocity = [bullet.velocity[0] * BULLET_SPEED, bullet.velocity[1] * BULLET_SPEED]

    bullets.append(bullet)

    #efectito del cursor al disparar 
    target.width += CURSOR_INCREASE_EFFECT
    target.height += CURSOR_INCREASE_EFFECT


def restart():
    #reiniciar el juego por completo 
    global player, enemies, bullets, particles, objects, score, is_game_over, boss, hearts

    objects.remove(player)
    start()

    #limpiar todos los enemigos
    for x in enemies:
        x.destroy()

    #limpiamos todas las balas 
    for x in bullets:
        objects.remove(x)
        bullets.remove(x)
        
    #limpiar todas las particulas     
    for x in particles:
        objects.remove(x)
        particles.remove(x)

    # Limpiar corazones
    for x in hearts:
        objects.remove(x)
    hearts.clear()

    # Limpiar jefe si existe
    if boss is not None:
        objects.remove(boss)
        boss = None

    score = 0
    load_high_score()
    is_game_over = False


def check_collisions(obj1, obj2):
    #verificamos las colisiones entre dos objetos 
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()

    # Si obj1 es el jefe, usamos sus hitboxes específicas
    if isinstance(obj1, Boss):
        for hitbox in obj1.hitboxes.values():
            hitbox_x = obj1.x + hitbox[0]
            hitbox_y = obj1.y + hitbox[1]
            if (hitbox_x <= x2 <= hitbox_x + hitbox[2] and
                hitbox_y <= y2 <= hitbox_y + hitbox[3]):
                return True
        return False
    
    # Si obj2 es el jefe, usamos sus hitboxes específicas
    if isinstance(obj2, Boss):
        for hitbox in obj2.hitboxes.values():
            hitbox_x = obj2.x + hitbox[0]
            hitbox_y = obj2.y + hitbox[1]
            if (hitbox_x <= x1 <= hitbox_x + hitbox[2] and
                hitbox_y <= y1 <= hitbox_y + hitbox[3]):
                return True
        return False

    #verificamos solapamiento en x
    if x1 + obj1.collider[0] / 2 > x2 - obj2.collider[0] / 2 and x1 - obj1.collider[0] / 2 < x2 + obj2.collider[0] / 2:
        #verificamos solapamiento en y 
        return y1 + obj1.collider[1] / 2 > y2 - obj2.collider[1] / 2 and y1 - obj1.collider[1] / 2 < y2 + obj2.collider[1] / 2
    return False


def handle_event(evt):
    #manejamos eventos de teclado y mouse 
    if evt.type == pygame.QUIT:
        exit()
    elif evt.type == pygame.KEYDOWN:
        #movimientos del jugador 
        if evt.key == pygame.K_a:
            player.velocity[0] = -player.speed
        elif evt.key == pygame.K_d:
            player.velocity[0] = player.speed
        elif evt.key == pygame.K_w:
            player.velocity[1] = -player.speed
        elif evt.key == pygame.K_s:
            player.velocity[1] = player.speed
        #controles del juego
        elif evt.key == pygame.K_r:
            restart()
        elif evt.key == pygame.K_SPACE:
            global has_game_started
            has_game_started = True
    elif evt.type == pygame.KEYUP:
        #detener movimiento del jugador 
        if evt.key == pygame.K_a or evt.key == pygame.K_d:
            player.velocity[0] = 0
        elif evt.key == pygame.K_w or evt.key == pygame.K_s:
            player.velocity[1] = 0
    elif evt.type == pygame.MOUSEBUTTONDOWN:
        shoot()


def display_ui():
    #mostramos interfaz
    if not has_game_started:
        #pantalla de inicio
        game_over_text = text_font.render(START_GAME_TEXT, True, BLACK)
        WINDOW.blit(game_over_text, (WINDOW_SIZE[0] / 2 - game_over_text.get_width() / 2,
                                     WINDOW_SIZE[1] / 2 - game_over_text.get_height() / 2))
        return

    #mostramos la vida(<3)
    for i in range(player.max_health):
        img = pygame.image.load(HEART_EMPTY if i >= player.health else HEART_FULL)
        img = pygame.transform.scale(img, (50, 50))
        WINDOW.blit(img, (i * 50 + WINDOW_SIZE[0] / 2 - player.max_health * 25, 25))

    #mostramos puntacion actual 
    score_text = text_font.render(f'Score: {score}', True, BLACK)
    WINDOW.blit(score_text, (score_text.get_width() / 2, 0 + 25))

    #mostramos puntacion maxima 
    high_score_text = text_font.render(f'High Score: {high_score}', True, BLACK)
    WINDOW.blit(high_score_text, (WINDOW_SIZE[0] - high_score_text.get_width() - 75, 0 + 25))

    #pantalla de cuando perdes
    if is_game_over:
        game_over_text = text_font.render(GAME_OVER_TEXT, True, BLACK)
        WINDOW.blit(game_over_text, (WINDOW_SIZE[0] / 2 - game_over_text.get_width() / 2,
                                     WINDOW_SIZE[1] / 2 - game_over_text.get_height() / 2))


def enemy_spawner():
    #generamos los enemigos depende de la puntacion y dificultad 
    global boss
    
    # Si el score llega a 25 y no hay jefe, creamos el jefe
    if score >= BOSS_SCORE_THRESHOLD and boss is None:
        # Posición aleatoria para el jefe
        randomX = random.randint(BOUNDS_X[0], BOUNDS_X[1] - BOSS_SIZE[0])
        randomY = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - BOSS_SIZE[1])
        boss = Boss(randomX, randomY, BOSS_SIZE[0], BOSS_SIZE[1], ENEMY_TILESET, BOSS_SPEED)
        # Efecto dramático de entrada
        for _ in range(3):
            spawn_particles(randomX + random.randint(0, BOSS_SIZE[0]),
                          randomY + random.randint(0, BOSS_SIZE[1]))
        offset = screen_shake(8, 10)
        return

    # Si hay un jefe, no generamos más enemigos
    if boss is not None:
        return
        
    if len(enemies) > (score + 10) // (10 / DIFFICULTY):
        return
    
    #posiciones randoms dentro de los limites 
    randomX = random.randint(BOUNDS_X[0], BOUNDS_X[1] - ENEMY_SIZE[0])
    randomY = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - ENEMY_SIZE[1])
    en = Enemy(randomX, randomY, ENEMY_SIZE[0], ENEMY_SIZE[1], ENEMY_TILESET, ENEMY_SPEED)
    
    #no generar enemigos muy cerca de nosotros 
    player_center = player.get_center()
    if abs(player_center[0] - en.x) < ENEMY_SPAWN_DISTANCE and abs(player_center[1] - en.y) < ENEMY_SPAWN_DISTANCE:
        objects.remove(en)
        #removemos la lista especifica de enemigos 
        enemies.remove(en)




#TEMBLEQUE DE PANTALLA 


#generador de tembleques, intensity es de la velocidas y amplitude es de la fuerza(distancia maxima)
def screen_shake(intensity, amplitude=20):
    #multiplicador para alterar direcciones 
    s = -1
    #hacemos 3 ciclos para completos de temblor 
    for _ in range(0, 3):
        #temblor hacia una direccion
        for x in range(0, amplitude, intensity):
            yield x * s, 0
        #temblor al centro 
        for x in range(amplitude, 0, intensity):
            yield x * s, 0
        #cambiar direccion para el siguiente ciclo 
        s *= -1

    #despues del temblequeo mantenemos la pantalla estable 
    while True:
        #sin offset, pantalla normal 
        yield 0, 0



#SISTEMA DE PARTICULAS 

#crear una particula enla posicion espedificada, usando cosas como explosiones
def spawn_particles(x, y):
    particle = Object(x, y, PARTICLES_SIZE[0], PARTICLES_SIZE[1], PARTICLES)
    #agregar a la lista de particulas activadas
    particles.append(particle)



#FUNCION DE ACTUALIZACION DE PANTALLA 

#actualizar la pantalla del juego con efectos de tembleque
def update_screen():
    #controlar fps
    clock.tick(FRAME_RATE)
    #aplicar el tembleque a la ventana principal
    #  offset viene del generador screen_shake
    SHAKE_WINDOW.blit(WINDOW, next(offset))
    #actualizamos display
    pygame.display.update()




#INICIALIZAMS RECURSOS 

#cargamos sprites
player_tileset = load_tileset(PLAYER_TILESET, 16, 16)
#usamos el primero como icono de la ventana 
pygame.display.set_icon(player_tileset[0][0])
#establecemos titulo de la ventana
pygame.display.set_caption(WINDOW_TITLE)

# Inicializar target antes del bucle principal
target = Object(100, 100, CURSOR_MIN_SIZE, CURSOR_MIN_SIZE, CURSOR)

#inicializamos el juego
start()





#BUCLE PRINCIPAL DEL JUEGO


while True:
    #MANEJO DE EVENTOS
    for event in pygame.event.get():
        #procesar input del usuario
        handle_event(event)

    #MANTENER EL JUGADOR DENTRO DE LOSLIMITES 
    #dentro de x
    player.x = max(BOUNDS_X[0], min(player.x, BOUNDS_X[1] - player.width))
    #dentro de y
    player.y = max(BOUNDS_Y[0], min(player.y, BOUNDS_Y[1] - player.height))


    #RENDERIZADO DE FONDO
    #cargar y escalar la imagen de fondo a resolucion de pantalla
    background = pygame.transform.scale(pygame.image.load(BACKGROUND), (1280, 720))
    #dibujar fondo de pantalla
    WINDOW.blit(background, (0, 0))

   
    #RENDERIZADO DE INTERFAZ DE USUARIO
    #mostrar vida, puntuacion, etc etc..
    display_ui()

    #ESTADO: JUEGO NO INICIADO
    if not has_game_started:
        #solo actualizar pantalla sin logica del juego 
        update_screen()
        #saltar resto del bucle
        continue


    #ESTADO: GAME OVER 
    if player.health <= 0:
        if not is_game_over:
            #ejecutar logica del fin del juego 
            game_over()
        #mostrat cursor del sistema
        pygame.mouse.set_visible(True)
        update_screen()
        #saltar el resto del bucle
        continue


    
    #MANEJO DE ORDEN DE RENDERIZADO
    #remover temporalmente para reordenamiento 
    objects.remove(target)
    #ordenar objetos por posicion y para simular profundidad 
    objects.sort(key=lambda o: o.y)
    #agregar targer al final para que se dibuje encima de todo
    objects.append(target)


    #SISTEMA DE PARTICULAS CON FADE OUT 
    for p in particles:
        #reducir trasparencia gradualmente 
        p.image.set_alpha(p.image.get_alpha() - 1)

        #si la particula es completamente trasparente borrarla 
        if p.image.get_alpha() == 0:
            objects.remove(p)
            particles.remove(p)
            continue

        #mover particula al frente para que se vea sobre otro objeto 
        objects.remove(p)
        #insertar al inicio de la lista
        objects.insert(0, p)



    #CONTROL DEL CURSOR/TARGET
    #ocultar cursor nomal de la compu
    pygame.mouse.set_visible(False)
    #obtener posicion del mouse
    mousePos = pygame.mouse.get_pos()

    #centrar targer en la posicion del mouse
    target.x = mousePos[0] - target.width / 2
    target.y = mousePos[1] - target.height / 2


    #ANIMACION DEL CURSOR 
    #reducir tamaño del cursor gradualmente hasta lo minimo 
    if target.width > CURSOR_MIN_SIZE:
        target.width -= CURSOR_SHRINK_SPEED
    if target.height > CURSOR_MIN_SIZE:
        target.height -= CURSOR_SHRINK_SPEED

    #ACTUALIZACION DE TODOS LOS OBJETOS 
    for obj in objects:
        #actualizar logica de cada objeto (movimienyo, animacion, etc etc...)
        obj.update()

    #LOGICA DE BALAS
    for b in bullets:
        #MODO REBOTE DE BALAS 
        if BULLETS_RICOCHET:
            #rebote horizontal
            if BOUNDS_X[0] > b.x or b.x > BOUNDS_X[1]:
                #invertir velocidad horizontal 
                b.velocity[0] *= -1
            #rebote vertical
            elif BOUNDS_Y[0] > b.y or b.y > BOUNDS_Y[1]:
                #invertir velocidad vertical
                b.velocity[1] *= -1
            continue

        #MODO NORMAL: DESTRUIR BALAS FUERA DE PANTALLA
        #si la bala esta dentro de los limites se continua 
        if BOUNDS_X[0] <= b.x <= BOUNDS_X[1] and BOUNDS_Y[0] <= b.y <= BOUNDS_Y[1]:
            continue

        #si esta fuera de limites destruir la bala
        bullets.remove(b)
        objects.remove(b)


    #LOGICA DE ENEMIGOS Y COLISIONES
    for e in enemies:
        #COLISION ENEMIGO/JUGADOR
        if check_collisions(e, player):
            #reducir vida del jugador 
            player.health -= 1
            #remover enemigo renderizado
            objects.remove(e)
            #remover enemigo de logica
            enemies.remove(e)
            #iniciar efecto de temblor
            offset = screen_shake(5)
            #crear particulas en posicion del enemigo
            spawn_particles(e.x, e.y)
            continue

        #COLISION ENEMIGO/BALA
        for b in bullets:
            if check_collisions(e, b):
                #dañar enemigo
                e.take_damage(1)
                #destruir bala
                bullets.remove(b)
                objects.remove(b)

    # COLISIONES CON CORAZONES
    for heart in hearts[:]:  # Usamos una copia de la lista para evitar problemas al modificarla
        if check_collisions(heart, player):
            if player.health < player.max_health:
                player.health += 1
                # Efecto visual de recolección
                spawn_particles(heart.x, heart.y)
                offset = screen_shake(3, 4)
            objects.remove(heart)
            hearts.remove(heart)

    #SPAWN DE NUEVOS ENEMIGOS
    #crear nuevos enemigos segun la logica del juehguito 
    enemy_spawner()

    # COLISIONES CON EL JEFE
    if boss is not None:
        # Colisión jefe/jugador
        if check_collisions(boss, player):
            player.health -= 2  # El jefe hace más daño
            offset = screen_shake(8)  # Temblor más fuerte
            spawn_particles(player.x, player.y)
            print("¡Colisión con el jefe!")  # Debug message

        # Colisión jefe/balas
        for b in bullets:
            if boss.check_hit(b):  # Usamos el sistema de hitboxes del jefe
                print("¡Bala golpeó al jefe!")  # Debug message
                bullets.remove(b)
                objects.remove(b)

    #ACTUALIZACION FINAL DE PANTALLA 
    #renderizar todo y actualizar display 
    update_screen()
