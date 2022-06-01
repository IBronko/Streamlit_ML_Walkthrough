import streamlit as st
from apps.start import start_app
from apps.webscraper import webscraper_app
from apps.eda import eda_app
from apps.training import training_app

page = st.sidebar.selectbox("Navigation", ("Project Description", "Data Acquisition", "EDA", "Model Training"))

if page == "Project Description":
    start_app()
elif page == "Data Acquisition":
    webscraper_app()
elif page == "EDA":
    eda_app()
elif page == "Model Training":
    training_app()