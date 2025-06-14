import pygame
import importlib
import os
from typing import Dict, Tuple, Optional

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.max_level = 4  # Número total de niveles
        self.levels: Dict[int, str] = {
            1: "level1",
            2: "level2",
            3: "level3",
            4: "level4"
        }
        self.current_level_module = None
        self.level_data = {
            "player_position": (640, 360),  # Posición inicial del jugador
            "player_health": 3,
            "player_score": 0
        }

    def load_level(self, level_number: int) -> bool:
        """
        Carga un nivel específico
        Retorna True si se cargó exitosamente, False si hubo error
        """
        if level_number not in self.levels:
            print(f"Error: Nivel {level_number} no existe")
            return False

        try:
            # Importar el módulo del nivel
            module_path = f"levels.{self.levels[level_number]}"
            self.current_level_module = importlib.import_module(module_path)
            
            # Actualizar el nivel actual
            self.current_level = level_number
            
            # Inicializar el nivel
            if hasattr(self.current_level_module, 'start'):
                self.current_level_module.start()
            
            print(f"Nivel {level_number} cargado exitosamente")
            return True

        except Exception as e:
            print(f"Error al cargar el nivel {level_number}: {str(e)}")
            return False

    def next_level(self) -> bool:
        """
        Avanza al siguiente nivel
        Retorna True si se avanzó exitosamente, False si no hay más niveles
        """
        if self.current_level >= self.max_level:
            print("¡Has completado todos los niveles!")
            return False

        next_level = self.current_level + 1
        return self.load_level(next_level)

    def previous_level(self) -> bool:
        """
        Retrocede al nivel anterior
        Retorna True si se retrocedió exitosamente, False si ya estamos en el primer nivel
        """
        if self.current_level <= 1:
            print("Ya estás en el primer nivel")
            return False

        prev_level = self.current_level - 1
        return self.load_level(prev_level)

    def get_current_level(self) -> int:
        """Retorna el número del nivel actual"""
        return self.current_level

    def save_level_state(self, player_position: Tuple[int, int], player_health: int, player_score: int):
        """Guarda el estado actual del nivel"""
        self.level_data = {
            "player_position": player_position,
            "player_health": player_health,
            "player_score": player_score
        }

    def get_level_state(self) -> Dict:
        """Retorna el estado guardado del nivel"""
        return self.level_data

    def is_level_completed(self) -> bool:
        """
        Verifica si el nivel actual está completado
        Retorna True si el nivel está completado, False si no
        """
        if not self.current_level_module:
            return False

        # Verificar si existe la variable is_victory en el módulo
        if hasattr(self.current_level_module, 'is_victory'):
            return self.current_level_module.is_victory
        return False

    def reset_level(self) -> bool:
        """
        Reinicia el nivel actual
        Retorna True si se reinició exitosamente
        """
        return self.load_level(self.current_level)

# Ejemplo de uso:
"""
# Crear el gestor de niveles
level_manager = LevelManager()

# Cargar el primer nivel
level_manager.load_level(1)

# En el bucle principal del juego:
while True:
    # ... código del juego ...

    # Si el nivel está completado, avanzar al siguiente
    if level_manager.is_level_completed():
        if not level_manager.next_level():
            # Si no hay más niveles, mostrar pantalla de victoria
            show_victory_screen()
            break

    # Si el jugador muere, reiniciar el nivel
    if player.health <= 0:
        level_manager.reset_level()
"""
