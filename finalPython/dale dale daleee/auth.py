import json
import os
from typing import Optional, Dict

class UserAuth:
    def __init__(self):
        self.users_file = "usuarios.json"
        self.current_user = None
        self._load_users()

    def _load_users(self) -> None:
        """Cargar usuarios desde archivo JSON o crear si no existe"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)
        
        with open(self.users_file, "r") as f:
            self.users = json.load(f)

    def _save_users(self) -> None:
        """Guardar usuarios en archivo JSON"""
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def register(self, username: str, password: str) -> Dict[str, str]:
        """Registrar un nuevo usuario"""
        if username in self.users:
            return {"status": "error", "message": "¡El usuario ya existe!"}
        
        self.users[username] = {
            "password": password,
            "high_score": 0
        }
        self._save_users()
        return {"status": "success", "message": "¡Usuario registrado exitosamente!"}

    def login(self, username: str, password: str) -> Dict[str, str]:
        """Iniciar sesión"""
        if username not in self.users:
            return {"status": "error", "message": "¡El usuario no existe!"}
        
        if self.users[username]["password"] != password:
            return {"status": "error", "message": "¡Contraseña incorrecta!"}
        
        self.current_user = username
        return {"status": "success", "message": "¡Inicio de sesión exitoso!"}

    def get_high_score(self, username: str) -> int:
        """Obtener puntaje más alto del usuario"""
        if username in self.users:
            return self.users[username]["high_score"]
        return 0

    def update_high_score(self, username: str, new_score: int) -> None:
        """Actualizar puntaje más alto si es mayor que el actual"""
        if username in self.users:
            if new_score > self.users[username]["high_score"]:
                self.users[username]["high_score"] = new_score
                self._save_users()

    def get_current_user(self) -> Optional[str]:
        """Obtener usuario actual"""
        return self.current_user

    def logout(self) -> None:
        """Cerrar sesión"""
        self.current_user = None 