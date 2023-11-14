import streamlit as st
import os
import sqlite3
import csv
from load_concerts import load_concerts

def admin_page(user_id):
    df_concerts = load_concerts(user_id)
    df_concerts.to_csv('concerts_data.csv')
    with open("concerts_data.csv", "rb") as f:
        st.download_button('Download Concerts', f, file_name='concerts_data.csv')  
    os.remove("concerts_data.csv")
