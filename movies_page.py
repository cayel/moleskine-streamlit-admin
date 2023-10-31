import streamlit as st
from load_movies import load_movies
from movies_list import movies_list

def movies_page(user_id):
    df_filtered_movies = load_movies(user_id)
    if not df_filtered_movies is None:
        if not df_filtered_movies.empty :
            tab1, tab2 = st.tabs(["Statistiques", "Données"])
            with tab1:
                st.header('Répartition des films par année', divider='blue')
                pivot_table = df_filtered_movies.pivot_table(index='annee', columns='cinema', values='id', aggfunc='count', fill_value=0)
                result = pivot_table.reset_index()
                result = result.rename(columns={0: 'Tv', 1: 'Cinéma'})
                st.bar_chart(pivot_table);
                col1, col2 = st.columns(2)

                director_counts = df_filtered_movies['director'].value_counts()
                top_10_directors = director_counts.head(10).sort_values(ascending=False)
                top_10_directors = top_10_directors.sort_values(ascending=False)
                with col1 : 
                    st.header("Les plus vus", divider='blue')
                    st.dataframe(top_10_directors, column_config={
                        "director": "Réalisateur",
                        "count": "Nombre"
                    }, hide_index=True, width=400)

                author_counts = df_filtered_movies['director'].value_counts()
                df_filtered_books_rating = df_filtered_movies[df_filtered_movies['director'].isin(author_counts[author_counts >= 3].index)]
                director_ratings = df_filtered_books_rating.groupby('director')['rating'].mean()
                director_ratings = director_ratings.round(2)
                top_10_directors = director_ratings.nlargest(10)
                with col2 : 
                    st.header("Les mieux notés", divider='blue')
                    st.dataframe(top_10_directors, column_config={
                        "director": "Réalisateur",
                        "rating": "Note"
                    }, hide_index=True, width=400)

                recent_movies = df_filtered_movies.sort_values(by='date', ascending=False)
                top_10_recent_movies = recent_movies.head(10)
                selected_columns = top_10_recent_movies[['director', 'title','cinema']]
                st.header("Les 10 derniers films vus", divider='blue')
                st.dataframe(selected_columns,    
                    column_config={
                        "director": "Réalisateur",
                        "title": "Titre",
                        "cinema": st.column_config.CheckboxColumn(
                            "Cinéma ?",
                            help="Vu au cinéma ou à la télévision",
                            default=False,
                            )
                    },
                hide_index=True, width=800)
            with tab2:
                movies_list(df_filtered_movies)
        else:
            st.write('Aucun film trouvé pour cet utilisateur.')
