##########################
# Import libraries/modules
##########################

import streamlit as st
from apps.helper_functions import *


def eda_app():
     
    st.write("Session State")
    st.write(st.session_state)
    
    df = load_raw_data()
    df_clean, missing_before, missing_after = load_cleaned_data()
    
    st.title("Explanatory data analysis")
    
    ######################################
    # Selection
    ######################################
    
    step = st.radio(
     "Check out one after another",
     ('Raw data', 
      'Cleaned data', 
      'Summary statistics',
      ))
    
    ######################################
    # Show raw data
    ######################################
    
    st.title("Raw data")
    st.write(df.head(10))
    st.text(f"Number of columns: {df.shape[1]}\nNumber of rows (samples): {df.shape[0]}")
    with st.expander("See explanation"):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)
                
    ####################################
    # Show cleaned data
    ####################################
    
    st.title("Cleaned Data")
   
    st.write(df_clean.head(10))
    st.text(f"Number of columns: {df_clean.shape[1]}")
    st.text(f"Number of rows: {df_clean.shape[0]}")

    def convert_df(df_clean):
        return df_clean.to_csv().encode('utf-8')
            
    csv_cleaned = convert_df(df_clean)
    st.download_button(
            label="Download cleaned data as .csv file",
            data=csv_cleaned,
            file_name='data_cleaned.csv',
            mime='text/csv',
            )
    
    st.plotly_chart(missing_before, use_container_width=True)
    st.plotly_chart(missing_after, use_container_width=True)
    with st.expander("See explanation"):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)
    
    ####################################
    # Show summary statistics
    ####################################

    st.title("Summary statistics")
    st.table(round(df_clean.describe().T,2))
    with st.expander("See explanation"):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)
    
    ####################################
    # Pieplot
    ####################################
    st.title("Explore target column")
    
    plot_pieplot(df_clean)
    with st.expander("See explanation"):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)
        
    ####################################
    # Histograms
    ####################################
    st.title("Target distribution")
    
    plot_histogram(df_clean)
    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
    
    ####################################
    # Correlation Heatmap
    ####################################
    
    st.title("Feature correlations")
    plot_corr_heatmap(df_clean)    
    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
    
    ####################################
    # Parallel Coordinate Plot
    ####################################
    
    plot_para_coordinate(df_clean)
    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
    
    ####################################
    # Scatter Plot
    ####################################
    
    plot_scatter(df_clean)
    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
    
    ####################################
    # Wordcloud
    ####################################
    
    plot_wordcloud(df_clean)    
    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)