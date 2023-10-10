import streamlit as st
import sqlite3

def select_user():
    conn = sqlite3.connect('moleskine.db')
    cursor = conn.cursor()    
    st.sidebar.title('Sélection de l\'utilisateur')
    users_query = "SELECT DISTINCT id, name FROM users"
    user_data = cursor.execute(users_query).fetchall()
    user_names = [user[1] for user in user_data]  # Liste des noms d'utilisateurs
    conn.close()

    # Utilisez la selectbox pour afficher les noms d'utilisateurs et récupérer l'ID sélectionné
    selected_user_index = st.sidebar.selectbox('Choisissez un utilisateur', user_names)
    selected_user_id = user_data[user_names.index(selected_user_index)][0]  # Récupérez l'ID correspondant au nom sélectionné    
    return selected_user_id

