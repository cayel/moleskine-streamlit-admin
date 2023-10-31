import streamlit as st
import datetime
from load_concerts import load_concerts
from load_books import load_books
from load_movies import load_movies

def dashboard_page(user_id):
    df_filtered_books = load_books(user_id)
    df_filtered_concerts = load_concerts(user_id)
    df_filtered_movies = load_movies(user_id)

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
    if not df_filtered_movies is None :
        year_counts = df_filtered_movies['annee'].value_counts().reset_index()
        year_counts.columns = ['Year', 'Film Count']
        movies_current_year = year_counts[year_counts['Year'] == current_year]['Film Count'].values
        movies_last_year = year_counts[year_counts['Year'] == last_year]['Film Count'].values
        if len(movies_current_year) > 0:
            movies_current_year = movies_current_year[0]
        else : 
            movies_current_year = 0
        if len(movies_last_year) > 0:
            movies_last_year = movies_last_year[0]
        else : 
            movies_last_year = 0
        delta = movies_current_year-movies_last_year
        col3.metric(label="Films", value=movies_current_year, delta=str(delta))
    st.header('Depuis la nuit des temps !', divider='blue')
    col1, col2, col3 = st.columns(3)
    if not df_filtered_books is None :
        col1.metric(label="Livres", value=len(df_filtered_books))
    if not df_filtered_concerts is None :
        col2.metric(label="Concerts", value=len(df_filtered_concerts))
    if not df_filtered_movies is None :
        col3.metric(label="Films", value=len(df_filtered_movies))