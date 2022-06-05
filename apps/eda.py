##########################
# Import libraries/modules
##########################

import streamlit as st
from apps.helper_functions import *


def eda_app():

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
     "Selection:",
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
        
        with st.expander("Notes"):
            st.markdown("""
                        This table shows a small fraction of the data, that has been scraped with Beautiful soup and saved as a .csv file.
                        Before building a model based on this data, some things need to be done before. 
                        
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
        
        with st.expander("Notes"):
            st.markdown("""
                        - :scissors: Every column with a missing value count above 500 has been removed
                        - :construction: The remaining missing values will be taken care of (imputed) in the model pipeline later on
                        - :checkered_flag: The last column of the table holds the encoded target variable called 'overall_number'
                        - :x: Comments have not been translated, as they will not be considered for the model
                        """)
        
    elif step == "Summary statistics":
            
        ####################################
        # Show summary statistics
        ####################################
        st.header("Summary statistics")
        
        st.dataframe(df_clean.describe().T.round(0))
        
        with st.expander("Notes"):
            st.markdown("""
                        - :checkered_flag: __Target (dependent) variable__: 
                        'overall_number' is a binary variable which can either be __1__ (employer recommended) or __0__ (employer not recommended). 
                        - :clipboard: __Feature (independent) variables__: 
                        Employees gave a ranking score between 1 (low) and 5 (high) for each feature. As the scale of measurement is __ordinal__ 'mean' and 'std' have to be taken with a grain of salt.
                        - :bar_chart: We need to work with __visualizations__ to get a better intuition for the data. 
                        
                        """)
            st.caption("Select from the visualization options at the top.")
        
    elif step == "Pie plot":
        
        ####################################
        # Pieplot
        ####################################
        st.header("Pie plot")
        
        st.plotly_chart(plot_pieplot(df_clean), use_container_width=True)
        
        with st.expander("Notes"):
            st.markdown("""
                        - The dataset is imbalanced with respect to the target variable. "recommended" is the majority class. 
                        - This needs to be considered during model evaluation (Accuracy metric may not be suitable for classification tasks with imbalanced datasets)
                        - We do not want to train a model on a much larger number of only one of the classes so it will be less likely to successfully predict the other class 
                        """)
           
    elif step == "Histograms":       
     
        ####################################
        # Histograms
        ####################################
        st.header("Histograms")
        
        st.pyplot(plot_histogram(df_clean), clear_figure=True)
        
        with st.expander("Notes"):
            st.markdown("""
                        - All features show a similiar left skewed distribution pattern 
                        - Strong skewness (implies outliers) can have negative effects on a model's performance 
                        - Depending on the (statistical) model, the data needs to be transformed (e.g. log transformation) 
                        - Tree based models are fairly robust to outliers
                        """)
        
    elif step == "Heatmap":    
        
        ####################################
        # Correlation Heatmap
        ####################################
        st.header("Correlation Heatmap")
        
        st.plotly_chart(plot_corr_heatmap(df_clean) , use_container_width=True)
        
        with st.expander("Notes"):
            st.markdown("""
                        __User tip__: Want to see more of one specific feature pair? Check out the scatter plot.
                        - There is a fairly strong positive correlation between all features
                        - With respect to 'overall number' (target) communication seems to be higher correlated than other features
                        - The question is, do all of the features add value to the predictive performance of a machine learning model? We could think of reducing the number of features, but this topic is out of scope for this project.
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
            
        with st.expander("Notes"):
            st.markdown("""
                        __User tip__: Play around by shifting axis from left to right and marking areas of certain axis.
                        
                        - As the features are highly correlated this plot does not really help to discover patterns, or does it? 
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
        
        with st.expander("Notes"):
            st.markdown("""
                        __User tip__: Try out different combinations of features.
                        - This is a great way to get an intution of the association between two features
                        - The benefit of scatter plots gets even more obvious when working with continuous data (rather than discrete values like in this case)
                        - Dark circles respresent the combinations where employees have recommended an employer
                        - As one would expect, a large fraction of dark circles (but not all) are located at or above the main diagonal  
                        """)    
        
    elif step == "Word cloud":      
        
        ####################################
        # Wordcloud
        ####################################
        st.header("Word cloud")
        
        st.pyplot(plot_wordcloud(df_clean), clear_figure=True)
        
        with st.expander("Notes"):
            st.markdown("""
                            This was just for fun... 
                            The word cloud is based on simple word counts (and removal of stop words) of the comments column and it was too tedious to translate to english...
                            """)  