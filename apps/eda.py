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
    
    ######################################
    # Import raw data and get an overview
    ######################################
    
    @st.cache
    def load():
        data = pd.read_csv("./data/data_raw.csv")
        data = data.sample(frac=1).reset_index(drop=True)
        data = data.drop("Unnamed: 0", axis=1)
        return data
        
    df = load()
    
    st.title("Exploratory Data Analysis")
    st.header("1. Import raw data and get an overview")
    st.write(df.head(10))
    st.text(f"Number of columns: {df.shape[1]}\nNumber of rows (samples): {df.shape[0]}")
    
    ####################################
    # Basic data cleaning
    ####################################
    
    st.header("2. Basic data cleaning")
    st.subheader("Renaming and translation")
    
    df = df.rename(columns={
    'Employer': "employer",
    'Time': "record_date",
    'Comment': "comment",
    'Overall': "overall_result",
    'Interessante Aufgaben': 'interesting_tasks', 
    'Gleichberechtigung': 'equality',
    'Kommunikation': "communication",
    'Arbeitsbedingungen': "working_conditions",
    'Vorgesetztenverhalten': "supervisor_behavior",
    'Umgang mit älteren Kollegen': "dealing_w_older_colleagues",
    'Kollegenzusammenhalt': "colleague_cohesion",
    'Umwelt-/Sozialbewusstsein': "environmental_social awareness",
    'Gehalt/Sozialleistungen': "salary_benefits",
    'Karriere/Weiterbildung': "career_training",
    'Work-Life-Balance': "work_life_balance",
    'Image': "image",
    'Arbeitsatmosphäre': "work_atmosphere",
    'Respekt': "respect",
    'Variation': "variation",
    'Spaßfaktor': "fun_factor",
    'Aufgaben/Tätigkeiten': "tasks",
    'Die Ausbilder': "trainer",
    'Ausbildungsvergütung': "apprenticeship_pay",
    'Arbeitszeiten': "working_hours",
    'Karrierechancen': "career_opportunities",
    'Arbeitgeber-Kommentar': "employer_comment",
    'Herausforderung': "challenge",
    'Arbeitgeber-Kommentare': "employer_comments"   
    })

    df.overall_result.replace("Nicht empfohlen", "not_recommended", inplace=True)
    df.overall_result.replace("Empfohlen", "recommended", inplace=True)
    st.write(df.head(10))
    
    st.subheader("Handle missing values")
    
    df_missing = df.isna().sum().sort_values(ascending=False)
    missing_barchart = px.bar(df_missing,
                                title="Missing feature data before drop",                             
                                text_auto='.2s',
                                labels=dict(value="Counts", index="Features"),
                                color_discrete_sequence=px.colors.sequential.Emrld
                                )

    missing_barchart.update_layout({
                                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                    },
                                showlegend=False)

    st.plotly_chart(missing_barchart)
    st.text(f"Number of columns: {df.shape[1]}")
    st.text(f"Number of rows: {df.shape[0]}")
    
    # Drop every column with missing value counts above 500
    with st.echo():
        threshold = 500
        drop_list = df_missing[df_missing > threshold].index.to_list()
        df = df.drop(drop_list, axis=1).reset_index(drop=True)
    
    df_missing_new = df.isna().sum().sort_values(ascending=False)
    missing_barchart = px.bar(df_missing_new,
                            title="Missing feature data after drop",                             
                            text_auto='.2s',
                            labels=dict(value="Counts", index="Features"),
                            color_discrete_sequence=px.colors.sequential.Emrld
                            )

    missing_barchart.update_layout({
                            "plot_bgcolor": "rgba(0, 0, 0, 0)",
                            "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                },
                            showlegend=False)
    
    st.plotly_chart(missing_barchart)
    st.text(f"Number of columns: {df.shape[1]}\nNumber of rows (samples): {df.shape[0]}")
    
    # Encode the overall result to 1s and 0s in a separate column
    encoder = LabelEncoder()
    df["overall_number"] = encoder.fit_transform(df.overall_result)
    
    st.subheader("Dataframe after basic cleaning")
    st.write(df.head(10))
    
    #################### 
    # Download csv file
    ####################

    def convert_df(df):
        return df.to_csv().encode('utf-8')
        
    csv_cleaned = convert_df(df)
    st.download_button(
            label="Download cleaned data as .csv file",
            data=csv_cleaned,
            file_name='data_cleaned.csv',
            mime='text/csv',
            )
    
    ####################################
    # Quick EDA
    ####################################
    
    st.header("3. Quick EDA")
    st.subheader("Summary statistics")
    st.table(round(df.describe().T,2))
    
    st.subheader("Explore target column")
    
    ####################################
    # Pieplot
    ####################################
    
    y = list(df.overall_result.value_counts().index)
    x = list(df.overall_result.value_counts().values)
    fig_pie = px.pie(df, 
             title='Target distribution',
             values=x, 
             names=y, 
             hole=.3, 
             color_discrete_sequence=px.colors.sequential.Emrld)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("Explore feature columns")
    
    numerical_columns = df.select_dtypes("number").columns
    
    ####################################
    # Histograms
    ####################################
    
    sns.set(style="white")
    sns.set_palette("crest")
    sns.set_context("paper")
    plt.figure(figsize=(20, 20))
    for i, f in enumerate(numerical_columns):
        plt.subplot(4,4,i+1)
        plt.axis('off')
        plt.title(f.title().replace("_", " "), fontsize=15)
        sns.histplot(data=df[f], bins=5, discrete=True)

    plt.suptitle("Feature Distributions (Scale: 1 - 5)", fontsize=20)
    plt.subplots_adjust(hspace=0.2, wspace=0.5)
    st.pyplot(plt, clear_figure=True)
    
    ####################################
    # Correlation Heatmap
    ####################################
    
    corr_fig = px.imshow(round(df[numerical_columns].corr(),2), 
                    text_auto=True, 
                    aspect="auto", 
                    color_continuous_scale=px.colors.sequential.Emrld)
    st.plotly_chart(corr_fig, use_container_width=True)
    
    ####################################
    # Parallel Coordinate Plot
    ####################################
    
    df_fig = df[["salary_benefits", "supervisor_behavior", "overall_number"]]
    parall_fig = px.parallel_coordinates(
                                    df_fig,color="overall_number", 
                                    color_continuous_scale=px.colors.diverging.Tealrose,
                                    )
    st.plotly_chart(parall_fig, use_container_width=True)
    
    ####################################
    # Scatter Plot
    ####################################
    
    scatter_fig = px.scatter(
                        df_fig, 
                        x=df_fig.salary_benefits, 
                        y=df_fig.supervisor_behavior, 
                        color=df_fig.overall_number, 
                        color_continuous_scale=px.colors.sequential.Emrld
                         )

    scatter_fig.update_layout(
                        {"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"} ,                   
                        xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1),
                        yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1)
                        )
    st.plotly_chart(scatter_fig, use_container_width=True)
    
    ####################################
    # Wordcloud
    ####################################
    
    stop_words = stop_bag.split("\n")
    word_list = ",".join(df.comment.to_list())
    word_list = word_list.lower().split(" ")
    comments_cleaned = [word for word in word_list if word not in stop_words]
    comments_cleaned = ",".join(comments_cleaned)

    wordcloud = WordCloud(width=800, 
                        height=500, 
                        margin=1, 
                        background_color='white').generate(comments_cleaned)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=1, y=1)
    st.pyplot(plt, clear_figure=True)