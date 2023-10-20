import streamlit as st

def movies_list(df):
    st.dataframe(df.sort_values(by='date', ascending=False)[['imageUrl','date', 'director', 'title','cinema']],column_config={
        "imageUrl": st.column_config.ImageColumn(
            "Affiche", help="Affiche du film"
            ),
        "date": st.column_config.DateColumn(
            "Date",
            format="DD/MM/YYYY",
        ),
        "director": "Réalisateur",
        "title": "Titre",
        "cinema": st.column_config.CheckboxColumn(
            "Cinéma ?",
            help="Vu au cinéma ou à la télévision",
            default=False,
            )
    },
hide_index=True,
width=800)
