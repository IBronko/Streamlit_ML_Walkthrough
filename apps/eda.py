##########################
# Import libraries/modules
##########################

from sklearn.utils import shuffle
import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
from wordcloud import WordCloud
from data.stop_words import stop_bag
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from helper_functions import read_file, rename_columns, find_missing, drop_missing, translate_target


def app():
    
    st.write("Session State")
    st.write(st.session_state)
    
    ####################################
    # Load data and get an overview
    ####################################
    st.title("Exploratory Data Analysis")
    st.header("1. Get an overview")
    df = read_file("notebooks/data_acquisition/raw_data.csv")
    st.write(df.head(10))
    st.text(f"Number of columns: {df.shape[1]}")
    st.text(f"Number of rows (samples): {df.shape[0]}")
    st.text("Task: Translate column labels and 'Overall' result to english.")
    
    ####################################
    # Translation and cleaning
    ####################################
    
    st.header("2. Basic cleaning")
    df = rename_columns(df)
    #st.write(df.columns)

    missing_barchart = px.bar(find_missing(df),
                            title="Missing feature values before drop",                             
                            text_auto='.2s',
                            labels=dict(value="Counts", index="Features")
                            )
    missing_barchart.update_layout(showlegend=False)
    
    st.plotly_chart(missing_barchart, use_container_width=True)

    df = drop_missing(df, 500)
    
    missing_barchart = px.bar(find_missing(df),
                            title="Missing feature values after drop",                             
                            text_auto='.2s',
                            labels=dict(value="Counts", index="Features")
                            )
    missing_barchart.update_layout(showlegend=False)
    
    st.plotly_chart(missing_barchart, use_container_width=True)
    st.text(f"Number of columns: {df.shape[1]}")
    st.text(f"Number of rows (samples): {df.shape[0]}")
    
    # df = translate_target(df, "overall_result")