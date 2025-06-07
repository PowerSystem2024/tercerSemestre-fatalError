from pymongo import MongoClient
from typing import Optional, Dict
from datetime import datetime

class MongoDBAuth:
    def __init__(self):
        # Conectar a MongoDB Atlas - Reemplaza <db_password> con tu contraseña real
        self.client = MongoClient('mongodb+srv://game_user:gamer123@cluster0.sawrq3u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.db = self.client['dale_dale_game']
        self.users = self.db['users']
        
        # Crear índice único para username
        self.users.create_index('username', unique=True)
        
        self.current_user = None

    def register(self, username: str, password: str) -> Dict[str, str]:
        """Registrar un nuevo usuario"""
        try:
            self.users.insert_one({
                'username': username,
                'password': password,  # En producción, esto debería estar hasheado
                'high_score': 0,
                'created_at': datetime.utcnow(),
                'last_login': datetime.utcnow()
            })
            return {"status": "success", "message": "¡Usuario registrado exitosamente!"}
        except Exception as e:
            return {"status": "error", "message": "¡El usuario ya existe!"}

    def login(self, username: str, password: str) -> Dict[str, str]:
        """Iniciar sesión"""
        user = self.users.find_one({'username': username})
        if not user:
            return {"status": "error", "message": "¡El usuario no existe!"}
        
        if user['password'] != password:  # En producción, comparar hashes
            return {"status": "error", "message": "¡Contraseña incorrecta!"}
        
        # Actualizar último login
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
        self.client.close()

    def __del__(self):
        """Cerrar conexión con MongoDB al destruir el objeto"""
        if hasattr(self, 'mongo_auth'):
            self.mongo_auth.close() 