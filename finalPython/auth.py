import json
import os
from typing import Optional, Dict
from systems.mongodb_auth import MongoDBAuth

class UserAuth:
    def __init__(self):
        self.users_file = "usuarios.json"
        self.current_user = None
        
        # Inicializar MongoDB
        self.mongo_auth = MongoDBAuth()
        
        # Cargar usuarios existentes de JSON a MongoDB si es necesario
        self.migrate_users()

    def migrate_users(self):
        try:
            # Intentar cargar usuarios desde el archivo JSON
            with open(self.users_file, 'r') as f:
                json_users = json.load(f)
                
            # Migrar cada usuario a MongoDB
            for username, user_data in json_users.items():
                if not self.mongo_auth.user_exists(username):
                    self.mongo_auth.register(username, user_data["password"])
                    if "high_score" in user_data:
                        self.mongo_auth.update_high_score(username, user_data["high_score"])
            
            # Si la migración fue exitosa, renombrar el archivo
            if os.path.exists(self.users_file):
                os.rename(self.users_file, f"{self.users_file}.bak")
        except FileNotFoundError:
            pass  # No hay usuarios para migrar
        except Exception as e:
            print(f"Error durante la migración: {e}")

    def register(self, username: str, password: str) -> Dict[str, str]:
        """Registrar un nuevo usuario"""
        return self.mongo_auth.register(username, password)

    def login(self, username: str, password: str) -> Dict[str, str]:
        """Iniciar sesión"""
        result = self.mongo_auth.login(username, password)
        if result["status"] == "success":
            self.current_user = username
        return result

    def get_high_score(self, username: str) -> int:
        """Obtener puntaje más alto del usuario"""
        return self.mongo_auth.get_high_score(username)

    def update_high_score(self, username: str, new_score: int) -> None:
        """Actualizar puntaje más alto si es mayor que el actual"""
        self.mongo_auth.update_high_score(username, new_score)

    def get_current_user(self) -> Optional[str]:
        """Obtener usuario actual"""
        return self.current_user

    def logout(self) -> None:
        """Cerrar sesión"""
        self.current_user = None

    def __del__(self):
        """Cerrar conexión con MongoDB al destruir el objeto"""
        try:
            if hasattr(self, 'mongo_auth'):
                self.mongo_auth.close()
        except:
            pass  # Ignorar errores durante el cierre 