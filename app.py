import streamlit as st
from firebase_singleton import FirebaseSingleton
import sqlite3
from data_processing_concert import display_top_artists
from data_processing_concert import display_top_venues
from data_processing_concert import display_concerts_by_year
from data_processing_book import display_books_by_year
from load_concerts import load_concerts
from load_books import load_books
from select_user import select_user
from streamlit_option_menu import option_menu

# Le reste de votre code Streamlit
st.title('Moleskine')
firebase_instance = FirebaseSingleton()

selected_user_id = select_user()

if st.sidebar.button("Rafraîchir les données"):  
    from create_users import create_users
    from create_concerts import create_concerts
    from create_books import create_books
    create_users() 
    create_concerts()
    create_books()

with st.sidebar:
    selected_menu = option_menu("Menu principal", ["Accueil", 'Concerts', 'Livres'], 
        icons=['house','music-note', 'book'], menu_icon="journal-richtext", default_index=0)
    

if selected_menu == 'Concerts':
    df_filtered_concerts = load_concerts(selected_user_id)

    # Affichez le nombre d'enregistrements dans un widget Streamlit
    st.write(f"Nombre d'enregistrements dans la table 'concerts': {len(df_filtered_concerts)}")    

    # Histogramme du nombre de concerts par année
    if not df_filtered_concerts.empty:
        display_concerts_by_year(df_filtered_concerts)
        display_top_venues(df_filtered_concerts)    
        display_top_artists(df_filtered_concerts)
    else:
        st.write('Aucun concert trouvé pour cette utilisateur.')
elif selected_menu == 'Livres':       
    df_filtered_books = load_books(selected_user_id)

    # Affichez le nombre d'enregistrements dans un widget Streamlit
    st.write(f"Nombre d'enregistrements dans la table 'livres': {len(df_filtered_books)}")    

    # Histogramme du nombre de livres par année
    if not df_filtered_books.empty:
        display_books_by_year(df_filtered_books)
    else:
        st.write('Aucun livre trouvé pour cette utilisateur.')
else:
    st.write('Autre menu')
    



