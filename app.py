import streamlit as st
from firebase_singleton import FirebaseSingleton
import sqlite3
from data_processing_concert import display_top_artists
from data_processing_concert import display_top_venues
from data_processing_concert import display_concerts_by_year
from load_concerts import load_concerts
from load_books import load_books
from load_movies import load_movies
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
    from create_movies import create_movies
    create_users() 
    create_concerts()
    create_books()
    print('before create')
    create_movies()

with st.sidebar:
    selected_menu = option_menu("Menu principal", ["Accueil", 'Concerts', 'Livres', 'Films'], 
        icons=['house','music-note', 'book', 'film'], menu_icon="journal-richtext", default_index=0)
    
if selected_menu == 'Accueil':
    df_filtered_books = load_books(selected_user_id)
    df_filtered_concerts = load_concerts(selected_user_id)
    df_filtered_movies = load_movies(selected_user_id)

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
        print(df_filtered_movies)
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
elif selected_menu == 'Concerts':
    df_filtered_concerts = load_concerts(selected_user_id)
    df_filtered_concerts['allArtists'] = df_filtered_concerts['mainArtist'] + '+' + df_filtered_concerts['otherArtist']
    df_filtered_concerts['allArtists'] = df_filtered_concerts['allArtists'].str.rstrip('+')
    
    if not df_filtered_concerts is None : 
        # Histogramme du nombre de concerts par année
        if not df_filtered_concerts.empty:
            st.header('Répartition des concerts par année', divider='blue')
            grouped_by_year = df_filtered_concerts.groupby('annee')
            count_per_year = grouped_by_year.size().reset_index()
            st.bar_chart(count_per_year, x="annee");

            col1, col2 = st.columns(2)
            all_artists = df_filtered_concerts['allArtists'].str.split('+').explode()
            top_10_artists = all_artists.value_counts().head(10)
            with col1 : 
                st.header("Les plus vus", divider='blue')
                st.dataframe(top_10_artists)
                
            venue_counts = df_filtered_concerts['venue'].value_counts()
            top_10_venues = venue_counts.head(10).sort_values(ascending=False)
            top_10_venues = top_10_venues.sort_values(ascending=False)
            with col2 : 
                st.header("Lieux préférés", divider='blue')
                st.dataframe(top_10_venues)

            recent_concerts = df_filtered_concerts.sort_values(by='date', ascending=False)
            top_10_recent_concerts = recent_concerts.head(10)
            selected_columns = top_10_recent_concerts[['mainArtist']]
            st.header("Les 10 derniers concerts", divider='blue')
            st.dataframe(selected_columns)
            #display_top_venues(df_filtered_concerts)    
            #display_top_artists(df_filtered_concerts)
        else:
            st.write('Aucun concert trouvé pour cette utilisateur.')
elif selected_menu == 'Livres':       
    df_filtered_books = load_books(selected_user_id)
    if not df_filtered_books is None:
        if not df_filtered_books.empty :
            st.header('Répartition des lectures par année', divider='blue')
            grouped_by_year = df_filtered_books.groupby('annee')
            count_per_year = grouped_by_year.size().reset_index()
            st.bar_chart(count_per_year, x="annee");
        
            col1, col2 = st.columns(2)

            writer_counts = df_filtered_books['writer'].value_counts()
            top_10_writers = writer_counts.head(10).sort_values(ascending=False)
            top_10_writers = top_10_writers.sort_values(ascending=False)
            with col1 : 
                st.header("Les plus lus", divider='blue')
                st.table(top_10_writers)

            author_counts = df_filtered_books['writer'].value_counts()
            df_filtered_books_rating = df_filtered_books[df_filtered_books['writer'].isin(author_counts[author_counts >= 3].index)]
            writer_ratings = df_filtered_books_rating.groupby('writer')['rating'].mean()
            writer_ratings = writer_ratings.round(2)
            top_10_writers = writer_ratings.nlargest(10)
            with col2 : 
                st.header("Les mieux notés", divider='blue')
                st.table(top_10_writers)

            recent_books = df_filtered_books.sort_values(by='date', ascending=False)
            top_10_recent_books = recent_books.head(10)
            selected_columns = top_10_recent_books[['writer', 'title']]
            st.header("Les 10 dernières lectures", divider='blue')
            st.table(selected_columns)
        else:
            st.write('Aucun livre trouvé pour cet utilisateur.')
elif selected_menu == 'Films':       
    df_filtered_movies = load_movies(selected_user_id)
    if not df_filtered_movies is None:
        if not df_filtered_movies.empty :
            st.header('Répartition des films par année', divider='blue')
            #grouped_by_year = df_filtered_movies.groupby('annee')
            #count_per_year = grouped_by_year.size().reset_index()
            #st.bar_chart(grouped_by_year, x="annee");
            pivot_table = df_filtered_movies.pivot_table(index='annee', columns='cinema', values='id', aggfunc='count', fill_value=0)
            result = pivot_table.reset_index()
            result = result.rename(columns={0: 'Tv', 1: 'Cinéma'})
            print(result)
            st.bar_chart(pivot_table);
            col1, col2 = st.columns(2)

            director_counts = df_filtered_movies['director'].value_counts()
            top_10_directors = director_counts.head(10).sort_values(ascending=False)
            top_10_directors = top_10_directors.sort_values(ascending=False)
            with col1 : 
                st.header("Les plus vus", divider='blue')
                st.table(top_10_directors)

            author_counts = df_filtered_movies['director'].value_counts()
            df_filtered_books_rating = df_filtered_movies[df_filtered_movies['director'].isin(author_counts[author_counts >= 3].index)]
            director_ratings = df_filtered_books_rating.groupby('director')['rating'].mean()
            director_ratings = director_ratings.round(2)
            top_10_directors = director_ratings.nlargest(10)
            with col2 : 
                st.header("Les mieux notés", divider='blue')
                st.table(top_10_directors)

            recent_movies = df_filtered_movies.sort_values(by='date', ascending=False)
            top_10_recent_movies = recent_movies.head(10)
            selected_columns = top_10_recent_movies[['director', 'title']]
            st.header("Les 10 derniers films vus", divider='blue')
            st.table(selected_columns)
        else:
            st.write('Aucun film trouvé pour cet utilisateur.')
else:
    st.write('Autre menu')
    



