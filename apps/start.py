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
    
    st.markdown("1. :octopus: Scrape data from a public website")
    st.markdown("2. :1234: Analyze and preprocess data")
    st.markdown("3. :robot_face: Train a predictive model")
    st.markdown("4. :bar_chart: Evaluate the model performance")
    st.markdown("5. :globe_with_meridians: Deploy the model and make predictions")
