import streamlit as st
from multiapp import MultiApp
from apps import start, webscraper, eda, training 

app = MultiApp()
app.add_app("Project Description", start.app)
app.add_app("1. Data Acquisition", webscraper.app)
app.add_app("2. Exploratory Data Analysis", eda.app)
app.add_app("3. Training", training.app)

app.run()