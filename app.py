import streamlit as st
from firebase_singleton import FirebaseSingleton
from select_user import select_user
from streamlit_option_menu import option_menu
from books_page import books_page
from concerts_page import concerts_page
from movies_page import movies_page
from dashboard_page import dashboard_page

st.title('Moleskine')

firebase_instance = FirebaseSingleton()
selected_user_id = select_user()

if st.sidebar.button("Rafraîchir les données"):  
    from create_users import create_users
    from create_concerts import create_concerts
    from create_books import create_books
    from create_movies import create_movies
    create_users() 
    create_concerts()
    create_books()
    create_movies()

with st.sidebar:
    selected_menu = option_menu("Menu principal", ["Accueil", 'Concerts', 'Livres', 'Films'], 
        icons=['house','music-note', 'book', 'film'], menu_icon="journal-richtext", default_index=0)
    
if selected_menu == 'Accueil':
    dashboard_page(selected_user_id)
elif selected_menu == 'Concerts':
    concerts_page(selected_user_id)
elif selected_menu == 'Livres':       
    books_page(selected_user_id)
elif selected_menu == 'Films':       
    movies_page(selected_user_id)



