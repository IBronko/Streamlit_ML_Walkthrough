import streamlit as st

def training_app():
    
    st.write("Session State")
    st.write(st.session_state)
    
    st.title("Training a model")