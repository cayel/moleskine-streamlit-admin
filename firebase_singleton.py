import firebase_admin
from firebase_admin import credentials
import streamlit as st

# Créez une classe Singleton pour gérer l'initialisation Firebase
class FirebaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseSingleton, cls).__new__(cls)
            # Initialisation de Firebase
            cred = firebase_admin.credentials.Certificate({
    	        "type": st.secrets.type,
		        "private_key" : st.secrets.private_key,
		        "client_email" : st.secrets.client_email,
		        "token_uri" : st.secrets.token_uri
	        })
            firebase_admin.initialize_app(cred,{
		        "databaseURL": st.secrets.database_url
		    })
        return cls._instance
