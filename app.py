import streamlit as st
from apps.start import start_app
from apps.webscraper import webscraper_app
from apps.eda import eda_app
from apps.training import training_app

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

button_status_list = ["show_import", "show_clean"]

for status in button_status_list:
    if status not in st.session_state:
        st.session_state[status] = False

page = st.sidebar.selectbox("Navigation", ("Project Description", "Data Acquisition", "EDA", "Model Training"))

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