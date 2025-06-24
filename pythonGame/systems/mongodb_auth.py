import os
from dotenv import load_dotenv
from pymongo import MongoClient

class MongoDBAuth:
    def __init__(self):
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in .env file")
        self.client = MongoClient(mongo_uri)
        self.db = self.client.game_db
        self.users_collection = self.db.users

    def register_user(self, username, hashed_password):
        if self.users_collection.find_one({"username": username}):
            return False, "Username already exists."
        self.users_collection.insert_one({"username": username, "password": hashed_password, "high_score": 0, "current_level": 1})
        return True, "User registered successfully."

    def login_user(self, username, hashed_password):
        user = self.users_collection.find_one({"username": username, "password": hashed_password})
        if user:
            return True, "Login successful."
        return False, "Invalid username or password."

    def update_high_score(self, username, score):
        self.users_collection.update_one({"username": username}, {"$max": {"high_score": score}})
        return True, "High score updated."

    def get_user_data(self, username):
        return self.users_collection.find_one({"username": username})

    def update_current_level(self, username, level):
        self.users_collection.update_one({"username": username}, {"$set": {"current_level": level}})
        return True, "Current level updated."

    def get_top_10_scores(self):
        """Obtener el top 10 de puntuaciones de todos los jugadores"""
        top_scores = list(self.users_collection.find(
            {"high_score": {"$gt": 0}},  # Solo usuarios con puntuación > 0
            {"username": 1, "high_score": 1, "_id": 0}
        ).sort("high_score", -1).limit(10))
        return top_scores

    def get_best_score(self):
        """Obtener la mejor puntuación global"""
        best_score_doc = self.users_collection.find_one(
            {"high_score": {"$gt": 0}},
            {"username": 1, "high_score": 1, "_id": 0},
            sort=[("high_score", -1)]
        )
        return best_score_doc if best_score_doc else {"username": "N/A", "high_score": 0}

    def get_user_rank(self, username):
        """Obtener la posición del usuario en el ranking global"""
        user_data = self.get_user_data(username)
        if not user_data or user_data.get("high_score", 0) == 0:
            return None
        
        # Contar cuántos usuarios tienen puntuación mayor
        higher_scores = self.users_collection.count_documents({
            "high_score": {"$gt": user_data["high_score"]}
        })
        return higher_scores + 1  # +1 porque el ranking empieza en 1

    def close(self):
        self.client.close() 