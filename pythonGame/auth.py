import json
import os
import bcrypt
from systems.mongodb_auth import MongoDBAuth

class UserAuth:
    def __init__(self):
        self.db_auth = MongoDBAuth()
        self.users_file = 'usuarios.json'
        self._migrate_users()

    def _migrate_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                legacy_users = json.load(f)
            for username, data in legacy_users.items():
                # Hashear contraseña antes de migrar
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.db_auth.register_user(username, hashed_password)
            os.remove(self.users_file)
            print("Migrated users from usuarios.json to MongoDB.")

    def register(self, username, password):
        # Hashear contraseña antes de registrar
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        success, message = self.db_auth.register_user(username, hashed_password)
        return success, message

    def login(self, username, password):
        user_data = self.db_auth.get_user_data(username)
        if user_data:
            stored_hashed_password = user_data.get('password', '').encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                return True, "Login successful."
        return False, "Invalid username or password."

    def update_high_score(self, username, score):
        return self.db_auth.update_high_score(username, score)

    def get_user_data(self, username):
        return self.db_auth.get_user_data(username)

    def update_current_level(self, username, level):
        return self.db_auth.update_current_level(username, level)

    def get_top_10_scores(self):
        """Obtener el top 10 de puntuaciones"""
        return self.db_auth.get_top_10_scores()

    def get_best_score(self):
        """Obtener la mejor puntuación global"""
        return self.db_auth.get_best_score()

    def get_user_rank(self, username):
        """Obtener la posición del usuario en el ranking"""
        return self.db_auth.get_user_rank(username)

    def close(self):
        self.db_auth.close() 