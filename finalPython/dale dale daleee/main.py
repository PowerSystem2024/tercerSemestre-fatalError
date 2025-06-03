import pygame
import random
from itertools import repeat
from auth import UserAuth
import login

#inicializamos pygame
pygame.init()
pygame.font.get_init()

# autewnticacion de usuario 
auth = UserAuth()
current_user = login.main()
if not current_user:
    exit()


# CONSTANTES:


#modo debug 
IS_DEBUG = False

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
PLAYER_SIZE = ENEMY_SIZE = PARTICLES_SIZE = (72, 72)
BULLET_SIZE = (16, 16)

#config del cursor 
CURSOR_MIN_SIZE = 50
CURSOR_INCREASE_EFFECT = 25
CURSOR_SHRINK_SPEED = 3

#rutas de recursos 
BACKGROUND = "assets/background.png"
PLAYER_TILESET = "assets/player-Sheet.png"
ENEMY_TILESET = "assets/enemy-Sheet.png"
BULLET = "assets/bullet.png"
CURSOR = "assets/cursor.png"
HEART_FULL = "assets/heart.png"
HEART_EMPTY = "assets/heart_empty.png"
PARTICLES = "assets/particles.png"

#esto lo comento por que ya no se guarda en el txt
#SAVE_FILE = "save_file.txt"

#texto en la interfaz
START_GAME_TEXT = "Espacio para empezar"
GAME_OVER_TEXT = "Perdiste:C, R para reiniciar"

# config de balance del juego
DIFFICULTY = 1
PLAYER_MAX_HEALTH = 3
PLAYER_SPEED = 4
ENEMY_MAX_HEALTH = 3
ENEMY_SPEED = 1.5
BULLET_SPEED = 10
ENEMY_SPAWN_DISTANCE = 250
BULLETS_RICOCHET = False



#CONFIGURACION PARA PYGAME 


# config de pantalla con soporte de temblor 
SHAKE_WINDOW = pygame.display.set_mode(WINDOW_SIZE)
WINDOW = SHAKE_WINDOW.copy()
clock = pygame.time.Clock()

#fuente
text_font = pygame.font.Font("assets/font.otf", 32)

#contenedores globales
#objetos dibujables 
objects = [] 
#desplazamiento para temblor de pantalla 
offset = repeat((0, 0))



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
        self.tileset = load_tileset(tileset, 16, 16)
        self.direction = 0 #direccion actual 
        self.flipX = False #forma horizontal 
        self.frame = 0 #frame actual de animacion
        self.frames = [0, 1, 0, 2] #secuencia para que se vea el movimiento 
        self.frame_timer = 0 #temporizador para velocidad de animacion 

    def change_direction(self):
        #actualizamos direcciones del sprite depende de la velocidad 
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipX = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipX = False
        elif self.velocity[1] > 0:
            self.direction = DOWN
        elif self.velocity[1] < 0:
            self.direction = UP

    def draw(self):
        #se dibuja el sprite con la direccion correcta 
        img = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width, self.height))

        self.change_direction()
 
        #lo ponemos horizontal si es necesario 
        img = pygame.transform.flip(img, self.flipX, False)
        WINDOW.blit(img, (self.x, self.y))

        #caja de colision 
        if IS_DEBUG:
            x, y = self.get_center()
            pygame.draw.rect(WINDOW, RED, (x - self.collider[0] / 2, y - self.collider[1] / 2, self.collider[0], self.collider[1]), width=1)

        #tiempo de animacion 
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            #se para la animacion cuando se frena 
            self.frame = 0
            return

        self.frame_timer += 1
       
        #control de velocidad de ainimacion 
        if self.frame_timer < 10:
            return

        #avanzmoas al siguiente frame 
        self.frame += 1
        if self.frame >= 4:
            self.frame = 0

        self.frame_timer = 0




#FUNCIONES UTILITARIAS 


def load_tileset(filename, width, height):
    #cargar la imagen tileset en tiles individuales 
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0, image_width // width):
        line = []
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset



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
        #propiedades de amimacioin de crecimiento 
        #ancho objetivo
        self.m_width = width
        #alto objetivo
        self.m_height = height
        #empezar invisible
        self.width = 0
        self.height = 0
        self.grow_speed = 2

        #una cajita de colicion mas chiquita para mejor jugabilidad 
        self.collider = [width / 2.5, height / 1.5]
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
        self.velocity = [self.velocity[0] / length, self.velocity[1] / length]
        self.velocity = [self.velocity[0] * self.speed, self.velocity[1] * self.speed]

        super().update()

    def change_direction(self):
        #logica de direccion personalizada para enemigos 
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipX = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipX = False


        #direccion vertical solo cuando es dominante 
        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] < 0:
            self.direction = UP

    def take_damage(self, damage):
        #manejamos el resibir daño y destruccion
        self.health -= damage
        if self.health > 0:
            return

        #efectos de muerte
        global score, offset
        score += 1
        #tiembla la pantalla
        offset = screen_shake(6, 7)
        #particulas de muerte 
        spawn_particles(self.x, self.y)

        self.destroy()

    def destroy(self):
        #sacar enemigo del jogo 
        objects.remove(self)
        enemies.remove(self)





# OBJETOS GLOBALES DEL JUEGO 


#cursor para apuntar 
global player, bullets
target = Object(100, 100, CURSOR_MIN_SIZE, CURSOR_MIN_SIZE, CURSOR)
#lista de todos los enemigos
enemies = []
#lista de efecto de particulas
particles = []

#variables de estado del juego 
has_game_started = False
is_game_over = False




# FUNCIONES PRINCIPALES DEL JUEGO


def load_high_score():
    #cargar puntacion maxima desde la base de datos
    global high_score
    high_score = auth.get_high_score(current_user)


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
        auth.update_high_score(current_user, score)
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
    global player, enemies, bullets, particles, objects, score, is_game_over

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

    score = 0
    load_high_score()
    is_game_over = False


def check_collisions(obj1, obj2):
    #verificamos las colisiones entre dos objetos 
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()

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
    if len(enemies) > (score + 10) // (10 / DIFFICULTY):
        return
    
    #posiciones randoms dentro de los limites 
    randomX = random.randint(BOUNDS_X[0], BOUNDS_X[1] - ENEMY_SIZE[0])
    randomY = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - ENEMY_SIZE[1])
    en = Enemy(randomX, randomY, ENEMY_SIZE[0], ENEMY_SIZE[1], ENEMY_TILESET, ENEMY_SPEED)
    
    #no generar enemigos muy cerca de nosotros 
    player_center = player.get_center() #este es centro del jugador para los calculos 
    #esto es para verificar que nosotros estamos en el rango de seguridad 
    if abs(player_center[0] - en.x) < ENEMY_SPAWN_DISTANCE and abs(player_center[1] - en.y) < ENEMY_SPAWN_DISTANCE:
        #removemos la lista de enemigos para renderizar 
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


    #SPAWN DE NUEVOS ENEMIGOS
    #crear nuevos enemigos segun la logica del juehguito 
    enemy_spawner()
    #ACTUALIZACION FINAL DE PANTALLA 
    #renderizar todo y actualizar display 
    update_screen()
