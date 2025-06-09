import json
import os
from typing import Optional, Dict
from systems.mongodb_auth import MongoDBAuth

class UserAuth:
    def __init__(self):
        # Mantener el archivo JSON para compatibilidad
        self.users_file = "usuarios.json"
        self.current_user = None
        
        # Inicializar MongoDB
        self.mongo_auth = MongoDBAuth()
        
        # Cargar usuarios existentes de JSON a MongoDB si es necesario
        self._migrate_users_if_needed()

    def _migrate_users_if_needed(self) -> None:
        """Migrar usuarios de JSON a MongoDB si es necesario"""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                json_users = json.load(f)
                
            # Migrar cada usuario a MongoDB
            for username, user_data in json_users.items():
                try:
                    self.mongo_auth.register(username, user_data["password"])
                    if "high_score" in user_data:
                        self.mongo_auth.update_high_score(username, user_data["high_score"])
                except:
                    # Si el usuario ya existe en MongoDB, lo ignoramos
                    pass

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
        self.mongo_auth.logout()

    def __del__(self):
        """Cerrar conexión con MongoDB al destruir el objeto"""
        if hasattr(self, 'mongo_auth'):
            self.mongo_auth.close() 