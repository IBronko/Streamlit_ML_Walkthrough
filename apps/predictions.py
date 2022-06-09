import streamlit as st
import pandas as pd
from joblib import dump, load
import time

def prediction_app():

    st.title("Make predictions")
    st.write("Time to make some predictions. Try different combinations and see, what the model predicts.")
    
    features = ['interesting_tasks', 
                'equality',
                'communication', 'working_conditions',
                'supervisor_behavior',
                'dealing_w_older_colleagues',
                'colleague_cohesion',
                'environmental_social awareness',
                'salary_benefits', 'career_training',
                'work_life_balance', 'image']
    
    scores = [1, 2, 3, 4, 5]
    
    with st.form("my_form"):  
        col1, col2 = st.columns(2)
        with col1:
            button_0 = st.radio(f"{features[0].title().replace('_', ' ')}",(scores), horizontal=True)
            button_1 = st.radio(f"{features[1].title().replace('_', ' ')}",(scores), horizontal=True)
            button_2 = st.radio(f"{features[2].title().replace('_', ' ')}",(scores), horizontal=True)
            button_3 = st.radio(f"{features[3].title().replace('_', ' ')}",(scores), horizontal=True)
            button_4 = st.radio(f"{features[4].title().replace('_', ' ')}",(scores), horizontal=True)
            button_5 = st.radio(f"{features[5].title().replace('_', ' ')}",(scores), horizontal=True)
        with col2:
            button_6 = st.radio(f"{features[6].title().replace('_', ' ')}",(scores), horizontal=True)
            button_7 = st.radio(f"{features[7].title().replace('_', ' ')}",(scores), horizontal=True)
            button_8 = st.radio(f"{features[8].title().replace('_', ' ')}",(scores), horizontal=True)
            button_9 = st.radio(f"{features[9].title().replace('_', ' ')}",(scores), horizontal=True)
            button_10 = st.radio(f"{features[10].title().replace('_', ' ')}",(scores), horizontal=True)
            button_11 = st.radio(f"{features[11].title().replace('_', ' ')}",(scores), horizontal=True)
        
        submitted = st.form_submit_button("Make prediction")
        
    if submitted:
        new_input = [button_0, button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10, button_11]
        new_input = pd.DataFrame([new_input], columns=features)
        #st.write(new_input)
        
        with st.spinner('Prediction started...'):
            time.sleep(2)
        
            saved_model = load('model/model.joblib') 
            
            st.subheader("Model prediction")
            
            if int(saved_model.predict(new_input)) == 1:
                st.balloons()
                st.markdown("Recommended :thumbsup:")
                
            elif int(saved_model.predict(new_input)) == 0:
                st.write("Not Recommended :thumbsdown:")
                
            st.subheader("Probability estimates")
            #st.write(saved_model.predict_proba(new_input))
            st.write(f"Recommended: {saved_model.predict_proba(new_input)[0][1]*100:.2f}%")
            st.write(f"Not recommended: {saved_model.predict_proba(new_input)[0][0]*100:.2f}%")