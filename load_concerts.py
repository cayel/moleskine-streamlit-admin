import sqlite3
import pandas as pd
import datetime
import os
from firebase_admin import db

def load_concerts_from_firebase(user_id):
    from firebase_singleton import FirebaseSingleton  
    ref = db.reference('concerts')
    data = ref.get()
    concerts_data = []
    
    if data:
        for utilisateur_id, utilisateur_data in data.items():
            if (user_id == utilisateur_id) :
                for concert_id, concert_data in utilisateur_data.items():
                    mainArtist = concert_data.get('mainArtist', 'Inconnu')
                    otherArtist = concert_data.get('otherArtist', 'Inconnu')
                    venue = concert_data.get('venue', 'Inconnu')
                    rating = concert_data.get('rating', 'Inconnu')
                    date = concert_data.get('date', 'Inconnu')
                    comment = concert_data.get('comment', '')
                    concerts_data.append({
                        'utiisateur_id': utilisateur_id,
                        'concert_id': concert_id,
                        'mainArtist': mainArtist,
                        'otherArtist': otherArtist,
                        'venue': venue,
                        'rating': rating,
                        'date': date,
                        'comment': comment
                    })
        concerts_df = pd.DataFrame(concerts_data)
        return concerts_df

def load_concerts(selected_user_id):
    if os.path.exists('moleskine.db'):
        conn = sqlite3.connect('moleskine.db')
        cursor = conn.cursor()
        
        concerts_query = "SELECT * FROM concerts WHERE utilisateur_id = ?"
        filtered_concerts = cursor.execute(concerts_query, (selected_user_id,)).fetchall()

        df_filtered_concerts = pd.DataFrame(filtered_concerts, columns=['id', 'utilisateur_id', 'mainArtist', 'otherArtist', 'venue', 'rating', 'date', 'comment'])
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
