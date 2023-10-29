import streamlit as st
from load_concerts import load_concerts
from concerts_list import concerts_list

def concerts_page(user_id):
    df_filtered_concerts = load_concerts(user_id)
    df_filtered_concerts['allArtists'] = df_filtered_concerts['mainArtist'] + '+' + df_filtered_concerts['otherArtist']
    df_filtered_concerts['allArtists'] = df_filtered_concerts['allArtists'].str.rstrip('+')
    
    if not df_filtered_concerts is None : 
        # Histogramme du nombre de concerts par année
        if not df_filtered_concerts.empty:
            tab1, tab2 = st.tabs(["Statistiques", "Données"])
            with tab1:
                st.header('Répartition des concerts par année', divider='blue')
                grouped_by_year = df_filtered_concerts.groupby('annee')
                count_per_year = grouped_by_year.size().reset_index()
                st.bar_chart(count_per_year, x="annee");

                col1, col2 = st.columns(2)
                all_artists = df_filtered_concerts['allArtists'].str.split('+').explode()
                top_10_artists = all_artists.value_counts().head(10)
                with col1 : 
                    st.header("Les plus vus", divider='blue')
                    st.dataframe(top_10_artists, column_config={
                        "allArtists": "Artiste",
                        "count": "Nombre"
                    }, hide_index=True, width=400)
                    
                venue_counts = df_filtered_concerts['venue'].value_counts()
                top_10_venues = venue_counts.head(10).sort_values(ascending=False)
                top_10_venues = top_10_venues.sort_values(ascending=False)
                with col2 : 
                    st.header("Lieux préférés", divider='blue')
                    st.dataframe(top_10_venues, column_config={
                        "venue": "Salle",
                        "count": "Nombre"
                    }, hide_index=True, width=400)

                recent_concerts = df_filtered_concerts.sort_values(by='date', ascending=False)
                top_10_recent_concerts = recent_concerts.head(10)
                selected_columns = top_10_recent_concerts[['mainArtist', 'venue']]
                st.header("Les 10 derniers concerts", divider='blue')
                st.dataframe(selected_columns, column_config={
                        "mainArtist": "Artiste",
                        "venue": "Salle"
                    }, hide_index=True, width=800)
            with tab2:
                concerts_list(df_filtered_concerts)   
        else:
            st.write('Aucun concert trouvé pour cette utilisateur.')
