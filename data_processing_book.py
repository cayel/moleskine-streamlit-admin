# data_processing.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

def display_books_by_year(df_filtered_books):
    df_pivot = df_filtered_books.pivot_table(index='annee', columns='rating', values='id', aggfunc='count', fill_value=0)
    # Créez un graphique à barres empilées
    sns.set()
    plt.figure(figsize=(10, 6))
    df_pivot.plot(kind='bar', stacked=True)
    plt.xlabel('Année')
    plt.ylabel('Nombre de livres')
    plt.title('Nombre de livres par année avec découpage par note')
    st.pyplot(plt)