import streamlit as st
from multiapp import MultiApp
from apps import webscraper, eda 

with st.sidebar:
    st.title("Project Description")
    
    st.markdown("""
This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). 
""")

app = MultiApp()

app.add_app("1. Data Acquisition", webscraper.app)
app.add_app("2. Exploratory Data Analysis", eda.app)

app.run()