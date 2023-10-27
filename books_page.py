import streamlit as st
from load_books import load_books
from books_list import books_list

def books_page(user_id):
    df_filtered_books = load_books(user_id)
    if not df_filtered_books is None:
        if not df_filtered_books.empty :
            tab1, tab2 = st.tabs(["Statistiques", "Données"])
            with tab1:
                st.header('Lectures par année', divider='blue')
                grouped_by_year = df_filtered_books.groupby('annee')
                count_per_year = grouped_by_year.size().reset_index()
                st.bar_chart(count_per_year, x="annee");
            
                col1, col2 = st.columns(2)

                writer_counts = df_filtered_books['writer'].value_counts()
                top_10_writers = writer_counts.head(10).sort_values(ascending=False)
                top_10_writers = top_10_writers.sort_values(ascending=False)
                with col1 : 
                    st.header("Les plus lus", divider='blue')
                    st.dataframe(top_10_writers, column_config={
                        "writer": "Auteur",
                        "count": "Nombre"
                    }, hide_index=True, width=400)

                author_counts = df_filtered_books['writer'].value_counts()
                df_filtered_books_rating = df_filtered_books[df_filtered_books['writer'].isin(author_counts[author_counts >= 3].index)]
                writer_ratings = df_filtered_books_rating.groupby('writer')['rating'].mean()
                writer_ratings = writer_ratings.round(2)
                top_10_writers = writer_ratings.nlargest(10)
                with col2 : 
                    st.header("Les mieux notés", divider='blue')
                    st.dataframe(top_10_writers, column_config={
                        "writer": "Auteur",
                        "rating": "Note"
                    }, hide_index=True, width=400)

                recent_books = df_filtered_books.sort_values(by='date', ascending=False)
                top_10_recent_books = recent_books.head(10)
                selected_columns = top_10_recent_books[['writer', 'title']]
                st.header("Les 10 dernières lectures", divider='blue')
                st.dataframe(selected_columns, column_config={
                    "writer": "Auteur",
                    "title": "Titre"
                }, hide_index=True, width=800)
            with tab2:
                books_list(df_filtered_books)
        else:
            st.write('Aucun livre trouvé pour cet utilisateur.')
