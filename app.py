import streamlit as st
import json
from streamlit_lottie import st_lottie
from apps.start import start_app
from apps.webscraper import webscraper_app
from apps.eda import eda_app
from apps.training import training_app
from apps.predictions import prediction_app

st.set_page_config(
     page_title="ML Walkthrough Project",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/IBronko/Streamlit_ML_Walkthrough',
         'Report a bug': "https://github.com/IBronko/Streamlit_ML_Walkthrough",
         'About': "# This is a personal project."
     }
 )

#####################################
# Initialize default session states
#####################################

button_status_list = ["start_scraping_button", "start_dummy_training_button"]

for status in button_status_list:
    if status not in st.session_state:
        st.session_state[status] = False

st.sidebar.title("End to end ML project")
page = st.sidebar.selectbox("Navigation", ("Project Description", "Data Acquisition", "EDA", "Model Training", "Make predictions"))

#####################################
# Display lottie file 
#####################################

def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
        
lottie_coding = load_lottiefile("images/lottie_start.json")

with st.sidebar:
    
    st_lottie(
        lottie_coding,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium", # medium ; high,
        key=None,
        )

    st.markdown("Code: [GitHub](https://github.com/IBronko/Streamlit_ML_Walkthrough.git)")
    st.markdown("Work in progress...")
    #st.write(st.session_state)

#####################################
# Import apps
#####################################

if page == "Project Description":
    start_app()
elif page == "Data Acquisition":
    webscraper_app()
elif page == "EDA":
    eda_app()
elif page == "Model Training":
    training_app()
elif page == "Make predictions":
    prediction_app()