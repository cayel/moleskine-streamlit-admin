import sqlite3
import pandas as pd
import datetime
import os


def load_books(selected_user_id):
    if os.path.exists('moleskine.db'):
        conn = sqlite3.connect('moleskine.db')
        cursor = conn.cursor()
        
        books_query = "SELECT * FROM books WHERE utilisateur_id = ?"
        filtered_books = cursor.execute(books_query, (selected_user_id,)).fetchall()

        df_filtered_books = pd.DataFrame(filtered_books, columns=['id', 'utilisateur_id', 'writer', 'title', 'rating', 'date'])
        if not df_filtered_books.empty:    
            # Convertissez la date en secondes (division par 1000)
            df_filtered_books['date'] = df_filtered_books['date'] / 1000
            # Convertissez les timestamps UNIX en objets datetime
            df_filtered_books['date'] = df_filtered_books['date'].apply(lambda x: datetime.datetime.fromtimestamp(x))
            # Extrait l'année de la date
            df_filtered_books['annee'] = df_filtered_books['date'].dt.year    
        conn.close()
        
        return df_filtered_books
    else :
        return None
