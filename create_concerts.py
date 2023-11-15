#cretae_concerts.py
from firebase_admin import db
import sqlite3

def create_concerts():
    from firebase_singleton import FirebaseSingleton  

    # Connexion à la base de données SQLite (créez-la s'il n'existe pas)
    conn = sqlite3.connect('moleskine.db')
    cursor = conn.cursor()

    # Suppression du contenu de la table concerts
    cursor.execute('''
            DROP TABLE IF EXISTS concerts
    ''')
    conn.commit()

    # Créez la table des concerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concerts (
            id TEXT PRIMARY KEY,
            utilisateur_id TEXT,
            mainArtist TEXT,
            otherArtist TEXT,
            venue TEXT,
            rating INTEGER,
            date DATE,
            comment TEXT
        )
    ''')
    conn.commit()

    ref = db.reference('concerts')

    data = ref.get()

    if data:
        for utilisateur_id, utilisateur_data in data.items():
            for concert_id, concert_data in utilisateur_data.items():
                mainArtist = concert_data.get('mainArtist', 'Inconnu')
                otherArtist = concert_data.get('otherArtist', 'Inconnu')
                venue = concert_data.get('venue', 'Inconnu')
                rating = concert_data.get('rating', 'Inconnu')
                date = concert_data.get('date', 'Inconnu')
                comment = concert_data.get('comment', '')
                # Insérez la commande dans la table SQLite des commandes
                cursor.execute('''
                    INSERT INTO concerts (id, utilisateur_id, mainArtist, otherArtist, date, venue, rating, comment)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (concert_id,utilisateur_id, mainArtist, otherArtist, date, venue, rating, comment))
                conn.commit()
        conn.close()
    else:
        conn.close()