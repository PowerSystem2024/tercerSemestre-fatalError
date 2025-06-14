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

    def close(self):
        self.client.close() 