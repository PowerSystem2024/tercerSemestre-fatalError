import os
import json

def get_users():
    db_path = os.path.join('db', 'users.json')
    if not os.path.exists('db'):
        os.makedirs('db')
    if not os.path.exists(db_path):
        with open(db_path, 'w') as f:
            json.dump({}, f)
    with open(db_path, 'r') as f:
        users = json.load(f)
    return users

def save_user(username):
    db_path = os.path.join('db', 'users.json')
    users = get_users()
    if username not in users:
        users[username] = {"niveles": 1}
        with open(db_path, 'w') as f:
            json.dump(users, f)

def user_login():
    # Ahora será gestionado desde el juego
    return None 