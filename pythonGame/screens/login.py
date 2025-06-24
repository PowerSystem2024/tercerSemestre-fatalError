import pygame
# from core.registry import get_users, save_user # Ya no es necesario

# --- Colores --- #
BG_COLOR = (40, 44, 52)        # Gris oscuro para el fondo (usaremos una imagen)
INPUT_BG_COLOR = (60, 65, 75)  # Gris un poco más claro para campos de entrada
TEXT_COLOR = (240, 240, 240)   # Gris muy claro para el texto
PLACEHOLDER_COLOR = (120, 120, 120) # Gris para el placeholder
BUTTON_COLOR = (50, 150, 200)  # Azul medio para el botón principal (Iniciar Sesión)
BUTTON_HOVER_COLOR = (70, 170, 220) # Azul más claro para el hover
REGISTER_BUTTON_COLOR = (80, 180, 100) # Verde medio para el botón de Registrar
REGISTER_BUTTON_HOVER_COLOR = (100, 200, 120) # Verde más claro para el hover
LEADERBOARD_BUTTON_COLOR = (200, 150, 50) # Naranja para el botón de ranking
LEADERBOARD_BUTTON_HOVER_COLOR = (220, 170, 70) # Naranja más claro para el hover
ERROR_COLOR = (255, 80, 80)    # Rojo para mensajes de error
SUCCESS_COLOR = (121, 195, 152) # Verde para mensajes de éxito
BORDER_COLOR = (80, 80, 80)    # Color del borde

# --- Fuentes --- #
pygame.font.init()
FONT_SMALL = pygame.font.Font(None, 28) # Ligeramente más pequeña
FONT_MEDIUM = pygame.font.Font(None, 36) # Ajustada
FONT_LARGE = pygame.font.Font(None, 50)  # Ligeramente más pequeña

def show_login(screen, user_auth):
    # Cargar y escalar la imagen de fondo
    background_image = pygame.image.load('assets/mapa/MENU.png').convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())

    # Rectángulos de los elementos (ajustados para mejor espaciado)
    input_box_user = pygame.Rect(screen.get_width()//2 - 170, screen.get_height()//2 - 80, 340, 45)
    input_box_pass = pygame.Rect(screen.get_width()//2 - 170, screen.get_height()//2 - 10, 340, 45)
    button_login = pygame.Rect(screen.get_width()//2 - 170, screen.get_height()//2 + 70, 160, 50)
    button_register = pygame.Rect(screen.get_width()//2 + 10, screen.get_height()//2 + 70, 160, 50)
    button_leaderboard = pygame.Rect(screen.get_width()//2 - 80, screen.get_height()//2 + 140, 160, 50)

    # Estado de los campos de entrada
    active_user = False
    active_pass = False
    username_text = ''
    password_text = ''
    message = ''
    message_color = ERROR_COLOR

    done = False
    clock = pygame.time.Clock()

    while not done:
        mouse_pos = pygame.mouse.get_pos()

        # Comprobar si el ratón está sobre los botones para el efecto hover
        hover_login = button_login.collidepoint(mouse_pos)
        hover_register = button_register.collidepoint(mouse_pos)
        hover_leaderboard = button_leaderboard.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic en campos de entrada
                active_user = input_box_user.collidepoint(event.pos)
                active_pass = input_box_pass.collidepoint(event.pos)

                # Clic en botones
                if button_login.collidepoint(event.pos):
                    if not username_text.strip() or not password_text.strip():
                        message = "Usuario y contraseña no pueden estar vacíos."
                        message_color = ERROR_COLOR
                    else:
                        success, msg = user_auth.login(username_text, password_text)
                        message = msg
                        message_color = SUCCESS_COLOR if success else ERROR_COLOR
                        if success:
                            print(f"Login successful: {username_text}")
                            return username_text
                elif button_register.collidepoint(event.pos):
                    if not username_text.strip() or not password_text.strip():
                        message = "Usuario y contraseña no pueden estar vacíos para registrarse."
                        message_color = ERROR_COLOR
                    else:
                        success, msg = user_auth.register(username_text, password_text)
                        message = msg
                        message_color = SUCCESS_COLOR if success else ERROR_COLOR
                        if success:
                            print(f"Registration successful: {username_text}")
                        else:
                            print(f"Registration failed: {msg}")
                elif button_leaderboard.collidepoint(event.pos):
                    # Mostrar ranking
                    from screens.leaderboard import show_leaderboard
                    show_leaderboard(screen, user_auth)

            if event.type == pygame.KEYDOWN:
                if active_user:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_user = False
                        active_pass = True # Mover al campo de contraseña
                    else:
                        username_text += event.unicode
                elif active_pass:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_pass = False
                        # Intentar login/registro al presionar ENTER en contraseña
                        if not username_text.strip() or not password_text.strip():
                            message = "Usuario y contraseña no pueden estar vacíos."
                            message_color = ERROR_COLOR
                        else:
                            success, msg = user_auth.login(username_text, password_text)
                            message = msg
                            message_color = SUCCESS_COLOR if success else ERROR_COLOR
                            if success:
                                print(f"Login successful: {username_text}")
                                return username_text
                    else:
                        password_text += event.unicode

        # --- Dibujar Fondo --- #
        screen.blit(background_image, (0, 0))

        # --- Dibujar Título --- #
        title_surface = FONT_LARGE.render('¡Bienvenido Jugador!', True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 180))
        screen.blit(title_surface, title_rect)

        # --- Dibujar campos de entrada --- #
        # Usuario
        pygame.draw.rect(screen, INPUT_BG_COLOR, input_box_user, border_radius=5)
        pygame.draw.rect(screen, BORDER_COLOR if not active_user else BUTTON_COLOR, input_box_user, 2, border_radius=5)
        user_label = FONT_SMALL.render('Usuario:', True, TEXT_COLOR)
        screen.blit(user_label, (input_box_user.x, input_box_user.y - 25))
        
        if username_text or active_user:
            txt_surface_user = FONT_MEDIUM.render(username_text, True, TEXT_COLOR)
            screen.blit(txt_surface_user, (input_box_user.x+10, input_box_user.y+8)) # Ajuste vertical
        else:
            placeholder_surface_user = FONT_MEDIUM.render('Escribe tu usuario', True, PLACEHOLDER_COLOR)
            screen.blit(placeholder_surface_user, (input_box_user.x+10, input_box_user.y+8)) # Ajuste vertical

        # Contraseña
        pygame.draw.rect(screen, INPUT_BG_COLOR, input_box_pass, border_radius=5)
        pygame.draw.rect(screen, BORDER_COLOR if not active_pass else BUTTON_COLOR, input_box_pass, 2, border_radius=5)
        pass_label = FONT_SMALL.render('Contraseña:', True, TEXT_COLOR)
        screen.blit(pass_label, (input_box_pass.x, input_box_pass.y - 25))
        
        if password_text or active_pass:
            txt_surface_pass = FONT_MEDIUM.render('*' * len(password_text), True, TEXT_COLOR) # Display asterisks
            screen.blit(txt_surface_pass, (input_box_pass.x+10, input_box_pass.y+8)) # Ajuste vertical
        else:
            placeholder_surface_pass = FONT_MEDIUM.render('Escribe tu contraseña', True, PLACEHOLDER_COLOR)
            screen.blit(placeholder_surface_pass, (input_box_pass.x+10, input_box_pass.y+8)) # Ajuste vertical

        # --- Dibujar botones --- #
        # Botón Iniciar Sesión
        current_login_color = BUTTON_HOVER_COLOR if hover_login else BUTTON_COLOR
        pygame.draw.rect(screen, current_login_color, button_login, border_radius=5)
        login_text_surface = FONT_MEDIUM.render('Iniciar Sesión', True, TEXT_COLOR)
        login_text_rect = login_text_surface.get_rect(center=button_login.center)
        screen.blit(login_text_surface, login_text_rect)

        # Botón Registrarse
        current_register_color = REGISTER_BUTTON_HOVER_COLOR if hover_register else REGISTER_BUTTON_COLOR
        pygame.draw.rect(screen, current_register_color, button_register, border_radius=5)
        register_text_surface = FONT_MEDIUM.render('Registrarse', True, TEXT_COLOR)
        register_text_rect = register_text_surface.get_rect(center=button_register.center)
        screen.blit(register_text_surface, register_text_rect)

        # Botón Ver Ranking
        current_leaderboard_color = LEADERBOARD_BUTTON_HOVER_COLOR if hover_leaderboard else LEADERBOARD_BUTTON_COLOR
        pygame.draw.rect(screen, current_leaderboard_color, button_leaderboard, border_radius=5)
        leaderboard_text_surface = FONT_MEDIUM.render('Ver Ranking', True, TEXT_COLOR)
        leaderboard_text_rect = leaderboard_text_surface.get_rect(center=button_leaderboard.center)
        screen.blit(leaderboard_text_surface, leaderboard_text_rect)

        # --- Mostrar mensaje (éxito/error) --- #
        if message:
            message_surface = FONT_SMALL.render(message, True, message_color) 
            message_rect = message_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 200)) # Ajuste vertical
            screen.blit(message_surface, message_rect)

        pygame.display.flip()
        clock.tick(30) 