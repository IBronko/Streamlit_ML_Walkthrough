import streamlit as st

def start_app():
    
    st.title("Project description")
    
    st.text("""
            The goal of this project is to build and deploy a predictive binary 
            classification model to answer the following question:
            """)
    
    st.text("""
            Based on certain questions about an employer, 
            can we predict if employees will recommend an employer or not?
            """)
    
    st.image("images/project_overview.png")