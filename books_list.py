import streamlit as st
import datetime

def create_search_field():
    search = st.text_input('Texte à rechercher')
    return search

def create_year_selector():
    current_year = datetime.datetime.now().year
    years_list = list(range(2009, current_year + 1))
    year_min, year_max = st.select_slider('Années de lecture', options=years_list, value=(2009, current_year))
    return year_min, year_max

def filter_data(df, search, year_min, year_max):
    mask_writer = df['writer'].str.contains(search, case=False)
    mask_title = df['title'].str.contains(search, case=False)
    filtered_df = df[mask_writer | mask_title]
    filtered_df = filtered_df.loc[(df['annee'] >= year_min) & (df['annee'] <= year_max)]
    return filtered_df

def display_filtered_data(filtered_df):
    st.dataframe(filtered_df.sort_values(by='date', ascending=False)[['imageUrl', 'date', 'writer', 'title', 'rating']], column_config={
        "imageUrl": st.column_config.ImageColumn("Affiche", help="Affiche du film"),
        "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
        "director": "Réalisateur",
        "title": "Titre",
        "rating": st.column_config.NumberColumn(
            "Note",
            help="Note attribuée",
            format="%d ⭐",
        ),
    }, hide_index=True, width=800, height=800)

def books_list(df):
    with st.container():
        search = create_search_field()
        year_min, year_max = create_year_selector()
    filtered_df = filter_data(df, search, year_min, year_max)
    display_filtered_data(filtered_df)

