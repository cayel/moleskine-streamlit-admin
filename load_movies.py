import sqlite3
import pandas as pd
import datetime
import os


def load_movies(selected_user_id):
    if os.path.exists('moleskine.db'):
        conn = sqlite3.connect('moleskine.db')
        cursor = conn.cursor()
        
        movies_query = "SELECT id, utilisateur_id, director, title, rating, date, cinema FROM movies WHERE utilisateur_id = ?"
        filtered_movies = cursor.execute(movies_query, (selected_user_id,)).fetchall()

        df_filtered_movies = pd.DataFrame(filtered_movies, columns=['id', 'utilisateur_id', 'director', 'title', 'rating', 'date', 'cinema'])
        if not df_filtered_movies.empty:    
            # Convertissez la date en secondes (division par 1000)
            df_filtered_movies['date'] = df_filtered_movies['date'] / 1000
            # Convertissez les timestamps UNIX en objets datetime
            df_filtered_movies['date'] = df_filtered_movies['date'].apply(lambda x: datetime.datetime.fromtimestamp(x))
            # Extrait l'année de la date
            df_filtered_movies['annee'] = df_filtered_movies['date'].dt.year   
            df_filtered_movies['cinema'] = df_filtered_movies['cinema'].map({True: 1, False: 0}) 
        conn.close()
        
        return df_filtered_movies
    else :
        return None
