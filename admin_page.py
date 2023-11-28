import streamlit as st
import os
import sqlite3
import csv
import load_concerts as lc
import time

def admin_page(user_id):
    df_concerts = lc.load_concerts(user_id)
    df_concerts.to_csv('concerts_data.csv')
    with open("concerts_data.csv", "rb") as f:
        st.download_button('Download Concerts', f, file_name='concerts_data.csv')  
    os.remove("concerts_data.csv")
    
    if st.button("Charger les données des concerts"):
        start_time = time.time()
        df = lc.load_concerts_from_firebase(user_id)
        elapsed_time = time.time() - start_time
        st.write("firebase : ",elapsed_time)
        start_time = time.time()
        df = lc.load_concerts(user_id)
        elapsed_time = time.time() - start_time
        st.write("sqlite : ",elapsed_time)
