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
import datetime

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
    
if selected_menu == 'Accueil':
    df_filtered_books = load_books(selected_user_id)
    df_filtered_concerts = load_concerts(selected_user_id)
    current_year = datetime.datetime.now().year
    last_year = current_year-1
    st.header('Cette année', divider='blue')
    col1, col2, col3 = st.columns(3)
    if not df_filtered_books is None :
        year_counts = df_filtered_books['annee'].value_counts().reset_index()
        year_counts.columns = ['Year', 'Book Count']
        books_current_year = year_counts[year_counts['Year'] == current_year]['Book Count'].values
        books_last_year = year_counts[year_counts['Year'] == last_year]['Book Count'].values
        if len(books_current_year) > 0:
            books_current_year = books_current_year[0]
        else : 
            books_current_year = 0
        if len(books_last_year) > 0:
            books_last_year = books_last_year[0]
        else : 
            books_last_year = 0
        delta = books_current_year-books_last_year
        col1.metric(label="Livres", value=books_current_year, delta=str(delta))
    if not df_filtered_concerts is None :
        year_counts = df_filtered_concerts['annee'].value_counts().reset_index()
        year_counts.columns = ['Year', 'Concert Count']
        concerts_current_year = year_counts[year_counts['Year'] == current_year]['Concert Count'].values
        concerts_last_year = year_counts[year_counts['Year'] == last_year]['Concert Count'].values
        if len(concerts_current_year) > 0:
            concerts_current_year = concerts_current_year[0]
        else : 
            concerts_current_year = 0
        if len(concerts_last_year) > 0:
            concerts_last_year = concerts_last_year[0]
        else : 
            concerts_last_year = 0
        delta = concerts_current_year-concerts_last_year
        col2.metric(label="Concerts", value=concerts_current_year, delta=str(delta))
    col3.metric(label="Films", value=0)    
    st.header('Depuis la nuit des temps !', divider='blue')
    col1, col2, col3 = st.columns(3)
    if not df_filtered_books is None :
        col1.metric(label="Livres", value=len(df_filtered_books))
    if not df_filtered_concerts is None :
        col2.metric(label="Concerts", value=len(df_filtered_concerts))
    col3.metric(label="Films", value=0)    
elif selected_menu == 'Concerts':
    df_filtered_concerts = load_concerts(selected_user_id)

    if not df_filtered_concerts is None : 
        # Histogramme du nombre de concerts par année
        if not df_filtered_concerts.empty:
            # Affichez le nombre d'enregistrements dans un widget Streamlit
            st.write(f"Nombre d'enregistrements dans la table 'concerts': {len(df_filtered_concerts)}")    

            display_concerts_by_year(df_filtered_concerts)
            display_top_venues(df_filtered_concerts)    
            display_top_artists(df_filtered_concerts)
        else:
            st.write('Aucun concert trouvé pour cette utilisateur.')
elif selected_menu == 'Livres':       
    df_filtered_books = load_books(selected_user_id)
    if not df_filtered_books is None:
        if not df_filtered_books.empty :
            # Affichez le nombre d'enregistrements dans un widget Streamlit
            st.write(f"Nombre d'enregistrements dans la table 'livres': {len(df_filtered_books)}")    

            # Histogramme du nombre de livres par année
            display_books_by_year(df_filtered_books)
        else:
            st.write('Aucun livre trouvé pour cet utilisateur.')
else:
    st.write('Autre menu')
    



