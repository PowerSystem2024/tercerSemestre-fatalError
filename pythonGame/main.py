import pygame
from core.game import Game
from screens.login import show_login
from auth import UserAuth
from systems.level_manager import LevelManager

IS_DEBUG = True  # Establecer en True para transiciones de nivel en modo depuración

def main():
    pygame.init()
    screen = pygame.display.set_mode((1064, 600))

    user_auth = UserAuth()
    usuario = show_login(screen, user_auth)  # Pasar user_auth a show_login

    if not usuario:
        print("Login failed or cancelled. Exiting.")
        return
    
    # Asumiendo que 'usuario' es la cadena del nombre de usuario después de un login exitoso
    current_username = usuario # Asignar el nombre de usuario a current_username

    level_manager = LevelManager(user_auth)
    # Cargar el último nivel guardado del usuario, o empezar en el nivel 1
    user_data = user_auth.get_user_data(current_username)
    initial_level_number = user_data.get("current_level", 1) if user_data else 1
    level_module = level_manager.load_level(initial_level_number, user_data) # Pasar user_data a load_level

    game = Game(current_username, level_manager, user_auth, initial_level_number, IS_DEBUG) # Pasar level_manager, user_auth y IS_DEBUG a Game
    game.run()

    user_auth.close() # Cerrar conexión a MongoDB

if __name__ == "__main__":
    main() 