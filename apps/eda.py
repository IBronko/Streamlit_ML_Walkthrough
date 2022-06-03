##########################
# Import libraries/modules
##########################

import streamlit as st
from apps.helper_functions import *


def eda_app():
     
    st.write(st.session_state)
    
    st.title("Explanatory data analysis")
    
    ######################################
    # Load data from helper functions
    ######################################
    
    df = load_raw_data()
    df_clean, missing_before, missing_after = load_cleaned_data()
    
    ######################################
    # Radio selection
    ######################################
    
    step = st.radio(
     "Select one option and toggle 'See explanation' button for more information.",
     ('Raw data', 
      'Cleaned data', 
      'Summary statistics',
      "Pie plot",
      "Histograms",
      "Heatmap",
      "Parallel coordinates",
      "Scatter plot",
      "Word cloud"
      ), horizontal=True)
    
    
    if step == "Raw data":
        
        ######################################
        # Show raw data
        ######################################
        st.header("Raw data")
        
        st.dataframe(df.head(10))
        st.text(f"Number of columns: {df.shape[1]}\nNumber of rows (samples): {df.shape[0]}")
        
        #Dowload csv file
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        
        csv_raw = convert_df(df)
        st.download_button(
                label="Download csv file",
                data=csv_raw,
                file_name='data_raw.csv',
                mime='text/csv',
                )
        
        with st.expander("See explanation"):
            st.markdown("""
                        This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                        
                        The next steps include the following preprocessing tasks:
                        
                        - :scissors: Find and drop columns with many missing values
                        - :pencil2: Translate german column lables to english
                        - :pencil2: Translate target values in column 'Overall' to english
                        - :hammer: Add encoded target variable (1s and 0s) in an additional column
                        """)
            
            st.caption("Select 'Cleaned data' from the selection above the see what the table looks like after those steps.")
        
    elif step == "Cleaned data":
                
        ####################################
        # Show cleaned data
        ####################################
        st.header("Cleaned Data")
    
        st.dataframe(df_clean.head(10))
        st.text(f"Number of columns: {df_clean.shape[1]}\nNumber of rows (samples): {df_clean.shape[0]}")

        #Dowload csv file
        def convert_df(df):
            return df.to_csv().encode('utf-8')
                
        csv_cleaned = convert_df(df_clean)
        st.download_button(
                label="Download csv file",
                data=csv_cleaned,
                file_name='data_cleaned.csv',
                mime='text/csv',
                )
        
        # Show plot
        st.plotly_chart(missing_before, use_container_width=True)
        st.plotly_chart(missing_after, use_container_width=True)
        
        with st.expander("See explanation"):
            st.markdown("""
                        This table shows a small fraction of the preprocessed data.
                        
                        The next steps include following preprocessing tasks:
                        
                        - :scissors: Find and drop columns with many missing values
                        - :pencil2: Translate german column lables to english
                        - :pencil2: Translate target values in column 'Overall' to english
                        - :hammer: Add encoded target variable (1s and 0s) in an additional column
                        
                        Select 'Cleaned data' from the selection above the see what the table looks like after those steps'
                        """)
        
    elif step == "Summary statistics":
            
        ####################################
        # Show summary statistics
        ####################################
        st.header("Summary statistics")
        
        st.dataframe(df_clean.describe().T.round(0))
        
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)
        
    elif step == "Pie plot":
        
        ####################################
        # Pieplot
        ####################################
        st.header("Pie plot")
        
        st.plotly_chart(plot_pieplot(df_clean), use_container_width=True)
        
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)
           
    elif step == "Histograms":       
     
        ####################################
        # Histograms
        ####################################
        st.header("Histograms")
        
        st.pyplot(plot_histogram(df_clean), clear_figure=True)
        
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)
        
    elif step == "Heatmap":    
        
        ####################################
        # Correlation Heatmap
        ####################################
        st.header("Correlation Heatmap")
        
        st.plotly_chart(plot_corr_heatmap(df_clean) , use_container_width=True)
        
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)   
        
    elif step == "Parallel coordinates":    
        
        ####################################
        # Parallel Coordinate Plot
        ####################################
        st.header("Parallel coordinates plot")
        
        p_plot_options = st.multiselect(
                                        "Select features to plot",
                                        [feature for feature in df_clean.select_dtypes("number").columns],
                                        ["salary_benefits", "dealing_w_older_colleagues"]
                                        )
        
        if len(p_plot_options) >=1:
            st.plotly_chart(plot_para_coordinate(df_clean, p_plot_options), use_container_width=True)
        else:
            st.error("Select at least one features to plot.")
            
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)
        
    elif step == "Scatter plot":      
        
        ####################################
        # Scatter Plot
        ####################################
        st.header("Scatter plot")
        
        scatter_col1, scatter_col2 = st.columns(2)
        
        with scatter_col1:
            x_option = st.selectbox(
                                "Select x-axis feature",
                                (feature for feature in df_clean.select_dtypes("number").columns), index=0, key="x_axis")
        with scatter_col2:
            y_option = st.selectbox(
                                "Select y-axis feature",
                                (feature for feature in df_clean.select_dtypes("number").columns), index=1, key="y_axis")
            
        st.plotly_chart(plot_scatter(df_clean, x_option, y_option), use_container_width=True)
        
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)    
        
    elif step == "Word cloud":      
        
        ####################################
        # Wordcloud
        ####################################
        st.header("Word cloud")
        
        st.pyplot(plot_wordcloud(df_clean), clear_figure=True)
        
        with st.expander("See explanation"):
            st.markdown("""
                            This table shows a small fraction of the data, that has been scrapped with Beautiful soup.
                            
                            The next steps include the following preprocessing tasks:
                            
                            - :scissors: Find and drop columns with many missing values
                            - :pencil2: Translate german column lables to english
                            - :pencil2: Translate target values in column 'Overall' to english
                            - :hammer: Add encoded target variable (1s and 0s) in an additional column
                            """)  