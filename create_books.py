#cretae_concerts.py
from firebase_admin import db
import sqlite3

def create_books():
    from firebase_singleton import FirebaseSingleton  

    # Connexion à la base de données SQLite (créez-la s'il n'existe pas)
    conn = sqlite3.connect('moleskine.db')
    cursor = conn.cursor()

    # Suppression du contenu de la table concerts
    cursor.execute('''
            DROP TABLE IF EXISTS books
    ''')
    conn.commit()

    # Créez la table des concerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            utilisateur_id TEXT,
            writer TEXT,
            title TEXT,
            rating INTEGER,
            date DATE
        )
    ''')
    conn.commit()

    ref = db.reference('books')

    data = ref.get()

    if data:
        for utilisateur_id, utilisateur_data in data.items():
            for book_id, book_data in utilisateur_data.items():
                writer = book_data.get('writer', 'Inconnu')
                title = book_data.get('title', 'Inconnu')
                rating = book_data.get('rating', 'Inconnu')
                date = book_data.get('date', 'Inconnu')
                # Insérez la commande dans la table SQLite des commandes
                cursor.execute('''
                    INSERT INTO books (id, utilisateur_id, writer, title, date, rating)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (book_id,utilisateur_id, writer, title, date, rating))
                conn.commit()
        conn.close()
    else:
        conn.close()