# create_users.py
from firebase_admin import db
import sqlite3

def create_users():
    # Initialisation de Firebase via le Singleton
    from firebase_singleton import FirebaseSingleton  

    # Connexion à la base de données SQLite (créez-la s'il n'existe pas)
    conn = sqlite3.connect('moleskine.db')
    cursor = conn.cursor()

    # Suppression du contenu de la table concerts
    cursor.execute('''
            DROP TABLE IF EXISTS users
    ''')
    conn.commit()

    # Création de la table des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT,
            name TEXT,
            username TEXT,
            last_connection DATE
        )
    ''')
    conn.commit()

    ref = db.reference('users')
    data = ref.get()

    if data:
        for utilisateur_id, utilisateur_data in data.items():
            email = utilisateur_data.get('email', 'Inconnu')
            name = utilisateur_data.get('name', 'Inconnu')
            username = utilisateur_data.get('username', 'Inconnu')
            last_connection = utilisateur_data.get('lastConnection', 'Inconnu')
            cursor.execute('''
                INSERT INTO users (id, email, name, username, last_connection)
                VALUES (?, ?, ?, ?, ?)
                ''', (utilisateur_id, email, name, username, last_connection))
            conn.commit()

        # Fermez la connexion à la base de données SQLite
        conn.close()
    else:
        conn.close()

