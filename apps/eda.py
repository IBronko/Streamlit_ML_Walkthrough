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


def eda_app():
    
    st.write("Session State")
    st.write(st.session_state)
    
    ####################################
    # Load data and get an overview
    ####################################
    df = pd.read_csv("./data/data_raw.csv")
    df = df.sample(frac=1).reset_index()
    df = df.drop("Unnamed: 0", axis=1)
    
    st.title("Exploratory Data Analysis")
    st.header("1. Get an overview")
    
    st.write(df.head(10))
    st.text(f"Number of columns: {df.shape[1]}")
    st.text(f"Number of rows (samples): {df.shape[0]}")
    
    missing_barchart = px.bar(df.isna().sum().sort_values(ascending=False),
                            title="Missing feature values before drop",                             
                            text_auto='.2s',
                            labels=dict(value="Counts", index="Features")
                            )
    missing_barchart.update_layout(showlegend=False)
    
    st.plotly_chart(missing_barchart, use_container_width=True)
    
    