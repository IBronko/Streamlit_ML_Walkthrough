import streamlit as st

def start_app():
    
    st.title("Project description")
    
    st.write("""
            The goal of this project is to build and deploy a predictive binary 
            classification model to answer the following question:
            """)
    
    st.write("""
            What is particularly important to employees about their employer so that they recommend it to others?
            """)
    
    st.subheader("Project Roadmap")
    st.image("images/project_overview.png")