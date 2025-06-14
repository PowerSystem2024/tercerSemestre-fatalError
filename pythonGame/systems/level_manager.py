import importlib
import os

class LevelManager:
    def __init__(self, user_auth):
        self.current_level_number = 1
        self.user_auth = user_auth
        self.levels_path = 'niveles'
        self.available_levels = self._load_available_levels()

    def _load_available_levels(self):
        levels = {}
        for filename in os.listdir(self.levels_path):
            if filename.startswith('nivel') and filename.endswith('.py'):
                try:
                    level_number = int(filename.replace('nivel', '').replace('.py', ''))
                    module_name = f'pythonGame.niveles.{filename[:-3]}'
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.levels_path, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    levels[level_number] = module
                except (ValueError, AttributeError) as e:
                    print(f"Error loading level file {filename}: {e}")
        return dict(sorted(levels.items()))

    def load_level(self, level_number, user_data):
        if level_number in self.available_levels:
            self.current_level_number = level_number
            level_module = self.available_levels[level_number]
            print(f"Loading level {level_number}")
            # Aquí es donde se llamaría una función en el módulo del nivel para configurarlo
            # Por ejemplo: level_module.setup_level(user_data)
            return level_module
        else:
            print(f"Level {level_number} not found.")
            return None

    def next_level(self, username):
        next_level_num = self.current_level_number + 1
        if next_level_num in self.available_levels:
            self.update_player_progress(username, next_level_num)
            return self.available_levels[next_level_num]
        else:
            print("No more levels available.")
            # Manejar la finalización del juego/pantalla de victoria aquí
            return None

    def previous_level(self, username):
        prev_level_num = self.current_level_number - 1
        if prev_level_num > 0 and prev_level_num in self.available_levels:
            self.update_player_progress(username, prev_level_num)
            return self.available_levels[prev_level_num]
        else:
            print("Already at the first level or level not found.")
            return None

    def update_player_progress(self, username, level_number):
        self.user_auth.update_current_level(username, level_number)
        self.current_level_number = level_number
        print(f"Player {username} progress updated to level {level_number}")

    def get_current_level_module(self):
        return self.available_levels.get(self.current_level_number)

    def get_current_level_number(self):
        return self.current_level_number 