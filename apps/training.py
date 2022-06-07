import streamlit as st
import pandas as pd
from apps.training_helper_functions import *
from apps.eda_helper_functions import load_cleaned_data
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
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
    
    model_step = st.radio(
     "Selection:",
     (
    'Data preprocessing',         
    'Baseline model',
    'Logistic Regression',
    'Model Evaluation'
      ), horizontal=True)
    
    drop_features = ["employer", "record_date", "comment", "overall_result", "overall_number"]
    target = df_clean.overall_number
    data = df_clean.drop(drop_features, axis=1)
        
    data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.25, random_state=123)
    target_names = ['recommended', 'not recommended']
    
    if model_step == "Data preprocessing":
        ######################################
        # Data preprocessing
        ######################################
        
        st.write("""
                 Before training a model and evaluating it's generalization performance the following steps are performed:
                 - Final definition of the features
                 - Split of samples into train- and test split (test split will only be used for the final evaluation)
                 - Definition of a preprocessing pipeline to handle missing values
                 """)
        
        st.header("Features")
        col1, col2 = st.columns(2)
        col1.metric("Total number of samples", target.shape[0])
        col2.metric("Total number of features", data.shape[1])
        st.write(f"Feature list:")
        st.write([column.title().replace("_", " ") for column in data.columns])

        st.header("Train-/ Test Split")
        col1, col2 = st.columns(2)
        col1.metric("Total number train samples", data_train.shape[0], "75%", delta_color="off")
        col2.metric("Total number test samples", data_test.shape[0], "25%", delta_color="off")
        
        st.header("Preprocessing pipeline")
        st.write("Scikit-Learn preprocessing pipeline:")
        st.code(make_preprocessor(data), language="python")
        
    if model_step == "Baseline model":
        ######################################
        # Baseline Model
        ######################################
        
        st.header("Dummy Classifier Pipeline")
        st.write("""
                This Scikit-Learn classifier serves as a simple baseline to compare against other more complex classifiers.
                The Dummy Classifier makes predictions that ignore the input features.
                """)
        dummy_pipeline = DummyPipe().pipe(data)
        
        
        
        def change_status_dummy_training():
          st.session_state.start_dummy_training = True 

        start_dummy_training_button = st.button("Start training and score model", on_click=change_status_dummy_training)  
          
        if start_dummy_training_button:
            dummy_pipeline.fit(data_train, target_train)
            dummy_pipe_predictions = dummy_pipeline.predict(data_test)
            
            score = accuracy_score(target_test, dummy_pipe_predictions)
            score2 = balanced_accuracy_score(target_test, dummy_pipe_predictions)
            st.write(f"Baseline accuracy score on test set: {score:.2f}%")
            st.write(f"Baseline balanced accuracy score on test set: {score2:.2f}%")
            
            with st.expander("Dummy Pipeline code details"):
              st.code(dummy_pipeline, language="python")
              st.caption("""
                     Before the data is fit on the DummyClassifier model, missing data is imputed.
                     """)