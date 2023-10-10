import sqlite3
import pandas as pd
import datetime
import os

def load_concerts(selected_user_id):
    if os.path.exists('moleskine.db'):
        conn = sqlite3.connect('moleskine.db')
        cursor = conn.cursor()
        
        concerts_query = "SELECT * FROM concerts WHERE utilisateur_id = ?"
        filtered_concerts = cursor.execute(concerts_query, (selected_user_id,)).fetchall()

        df_filtered_concerts = pd.DataFrame(filtered_concerts, columns=['id', 'utilisateur_id', 'mainArtist', 'otherArtist', 'venue', 'rating', 'date'])
        if not df_filtered_concerts.empty:    
            # Convertissez la date en secondes (division par 1000)
            df_filtered_concerts['date'] = df_filtered_concerts['date'] / 1000
            # Convertissez les timestamps UNIX en objets datetime
            df_filtered_concerts['date'] = df_filtered_concerts['date'].apply(lambda x: datetime.datetime.fromtimestamp(x))
            # Extrait l'année de la date
            df_filtered_concerts['annee'] = df_filtered_concerts['date'].dt.year    
        conn.close()
    
        return df_filtered_concerts
    else :
            return None
