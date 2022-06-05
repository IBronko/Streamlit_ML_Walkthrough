import streamlit as st
from apps.training_helper_functions import *
from apps.eda_helper_functions import load_cleaned_data
from sklearn.model_selection import train_test_split, cross_validate
from sklearn import set_config
set_config(display="text") #/diagram 


def training_app():
    
    st.title("Training a model")
    
    ######################################
    # Load data from helper functions
    ######################################
    
    df_clean, _, _ = load_cleaned_data()
    
    ######################################
    # Radio selection
    ######################################
    
    step = st.radio(
     "Selection:",
     (
    'Data preprocessing',         
    'Baseline model',
    'Logistic Regression',
    'Model Evaluation'
      ), horizontal=True)
    
    ######################################
    # Data preprocessing
    ######################################
    
    drop_features = ["employer", "record_date", "comment", "overall_result", "overall_number"]
    target = df_clean.overall_number
    data = df_clean.drop(drop_features, axis=1)
    
    data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.25, random_state=123)
    
    st.header("Stats cleaned data")
    col1, col2 = st.columns(2)
    col1.metric("Total number of samples", target.shape[0])
    col2.metric("Total number of features", data.shape[1])
    st.write(f"Feature list:")
    st.write([column.title().replace("_", " ") for column in data.columns])

    st.header("Stats Train-/ Test Split")
    col1, col2 = st.columns(2)
    col1.metric("Total number train samples", data_train.shape[0], "75%", delta_color="off")
    col2.metric("Total number test smaples", data_test.shape[0], "25%", delta_color="off")
    
    st.header("Handle missing values")
    st.write("Scikit-Learn preprocessing pipeline:")
    st.code(make_preprocessor(data), language="python")