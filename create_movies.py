#cretae_concerts.py
from firebase_admin import db
import sqlite3

def create_movies():
    from firebase_singleton import FirebaseSingleton  

    # Connexion à la base de données SQLite (créez-la s'il n'existe pas)
    conn = sqlite3.connect('moleskine.db')
    cursor = conn.cursor()

    # Suppression du contenu de la table concerts
    cursor.execute('''
            DROP TABLE IF EXISTS movies
    ''')
    conn.commit()
    print('before creation')

    # Créez la table des films
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id TEXT PRIMARY KEY,
            utilisateur_id TEXT,
            director TEXT,
            title TEXT,
            cinema BOOLEAN,      
            rating INTEGER,
            date DATE,
            imageUrl TEXT
        )
    ''')
    conn.commit()

    ref = db.reference('movies')

    data = ref.get()

    if data:
        for utilisateur_id, utilisateur_data in data.items():
            for movie_id, movie_data in utilisateur_data.items():
                director = movie_data.get('director', 'Inconnu')
                title = movie_data.get('title', 'Inconnu')
                rating = movie_data.get('rating', 'Inconnu')
                date = movie_data.get('date', 'Inconnu')
                cinema = movie_data.get('cinema',False)
                imageUrl = movie_data.get('imageUrl','Inconnu') 
                # Insérez la commande dans la table SQLite des commandes
                cursor.execute('''
                    INSERT INTO movies (id, utilisateur_id, director, title, date, rating, cinema, imageUrl)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (movie_id,utilisateur_id, director, title, date, rating, cinema, imageUrl))
            conn.commit()
        conn.close()
    else:
        conn.close()
