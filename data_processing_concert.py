# data_processing.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

def display_concerts_by_year(df_filtered_concerts):
    df_pivot = df_filtered_concerts.pivot_table(index='annee', columns='rating', values='id', aggfunc='count', fill_value=0)
    # Créez un graphique à barres empilées
    sns.set()
    plt.figure(figsize=(10, 6))
    df_pivot.plot(kind='bar', stacked=True)
    plt.xlabel('Année')
    plt.ylabel('Nombre de concerts')
    plt.title('Nombre de concerts par année avec découpage par note')
    st.pyplot(plt)

def display_top_venues(df_filtered_concerts):
    top_venues = df_filtered_concerts['venue'].value_counts().head(5)
    # Créez un graphique à barres pour afficher le top 5 des venues
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_venues.index, y=top_venues.values)
    plt.xlabel('Venue')
    plt.ylabel('Nombre de concerts')
    plt.title('Top 5 des lieux de concerts')
    plt.xticks(rotation=45)  # Rotation des labels de l'axe x pour une meilleure lisibilité
    st.pyplot(plt)
    pass

def display_top_artists(df_filtered_concerts):
    top_artists = df_filtered_concerts['mainArtist'].value_counts().head(5)
    # Créez un graphique à barres pour afficher le top 5 des venues
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_artists.index, y=top_artists.values)
    plt.xlabel('Artistes')
    plt.ylabel('Nombre de concerts')
    plt.title('Top 5 des artistes')
    plt.xticks(rotation=45)  # Rotation des labels de l'axe x pour une meilleure lisibilité
    st.pyplot(plt)
    pass
