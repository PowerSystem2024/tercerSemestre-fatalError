from pymongo import MongoClient
from typing import Optional, Dict
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib

# Cargar variables de entorno desde .env
load_dotenv()

class MongoDBAuth:
    def __init__(self):
        # Obtener la cadena de conexión desde las variables de entorno
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI no está configurada en el archivo .env o en las variables de entorno.")

        self.client = MongoClient(mongo_uri)
        self.db = self.client['dale_dale_game']
        self.users = self.db['users']
        
        # Crear índice único para username
        self.users.create_index('username', unique=True)
        
        self.current_user = None

    def register(self, username: str, password: str) -> Dict[str, str]:
        """Registrar un nuevo usuario"""
        if self.user_exists(username):
            return {"status": "error", "message": "¡Usuario ya existe!"}
        
        hashed_password = self._hash_password(password)
        self.users.insert_one({
            'username': username,
            'password': hashed_password,
            'high_score': 0,
            'created_at': datetime.utcnow(),
            'last_login': datetime.utcnow()
        })
        return {"status": "success", "message": "¡Usuario registrado exitosamente!"}

    def login(self, username: str, password: str) -> Dict[str, str]:
        """Iniciar sesión"""
        user = self.users.find_one({'username': username})
        if not user:
            return {"status": "error", "message": "¡El usuario no existe!"}
        
        if not self._verify_password(password, user['password']):
            return {"status": "error", "message": "¡Contraseña incorrecta!"}
        
        self.users.update_one(
            {'username': username},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        self.current_user = username
        return {"status": "success", "message": "¡Inicio de sesión exitoso!"}

    def get_high_score(self, username: str) -> int:
        """Obtener puntaje más alto del usuario"""
        user = self.users.find_one({'username': username})
        return user['high_score'] if user else 0

    def update_high_score(self, username: str, new_score: int) -> None:
        """Actualizar puntaje más alto si es mayor que el actual"""
        user = self.users.find_one({'username': username})
        if user and new_score > user['high_score']:
            self.users.update_one(
                {'username': username},
                {'$set': {'high_score': new_score}}
            )

    def get_current_user(self) -> Optional[str]:
        """Obtener usuario actual"""
        return self.current_user

    def logout(self) -> None:
        """Cerrar sesión"""
        self.current_user = None

    def close(self):
        """Cerrar la conexión con MongoDB"""
        try:
            if hasattr(self, 'client'):
                self.client.close()
        except:
            pass  # Ignorar errores durante el cierre

    def __del__(self):
        """Cerrar conexión con MongoDB al destruir el objeto"""
        if hasattr(self, 'mongo_auth'):
            self.mongo_auth.close()

    def user_exists(self, username: str) -> bool:
        """Verificar si el usuario ya existe"""
        return self.users.find_one({'username': username}) is not None

    def _hash_password(self, password: str) -> str:
        """Hashear la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verificar la contraseña hasheada"""
        return self._hash_password(password) == hashed 