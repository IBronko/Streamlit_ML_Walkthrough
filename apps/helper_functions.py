##########################
# Import libraries/modules
##########################

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from data.stop_words import stop_bag
import plotly.express as px
from sklearn.preprocessing import LabelEncoder


######################################
# Import raw data and get an overview
######################################

@st.cache
def load_raw_data():
    df = pd.read_csv("./data/data_raw.csv")
    df = df.sample(frac=1).reset_index(drop=True)
    df = df.drop("Unnamed: 0", axis=1)
    return df

####################################
# Basic data cleaning
####################################

@st.cache(allow_output_mutation=True)
def load_cleaned_data():
    df_clean = load_raw_data()
    
    # Translate columns
    df_clean = df_clean.rename(columns={
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
    
    # Translate overall results
    df_clean.overall_result.replace("Nicht empfohlen", "not_recommended", inplace=True)
    df_clean.overall_result.replace("Empfohlen", "recommended", inplace=True)
    
    # Plot missing before cleaning
    df_missing_before = df_clean.isna().sum().sort_values(ascending=False)
    missing_barchart_before = px.bar(df_missing_before,
                                title="Missing feature data before drop",                             
                                text_auto='.2s',
                                labels=dict(value="Counts", index="Features"),
                                color_discrete_sequence=px.colors.sequential.Emrld
                                )

    missing_barchart_before.update_layout({
                                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                    },
                                showlegend=False)
    
    # Drop missing columns
    threshold = 500
    drop_list = df_missing_before[df_missing_before > threshold].index.to_list()
    df_clean = df_clean.drop(drop_list, axis=1).reset_index(drop=True)
    
    # Plot missing before cleaning
    df_missing_new = df_clean.isna().sum().sort_values(ascending=False)
    missing_barchart_after = px.bar(df_missing_new,
                            title="Missing feature data after drop",                             
                            text_auto='.2s',
                            labels=dict(value="Counts", index="Features"),
                            color_discrete_sequence=px.colors.sequential.Emrld
                            )

    missing_barchart_after.update_layout({
                            "plot_bgcolor": "rgba(0, 0, 0, 0)",
                            "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                },
                            showlegend=False)
    
    # Encode the overall result to 1s and 0s in a separate column
    encoder = LabelEncoder()
    df_clean["overall_number"] = encoder.fit_transform(df_clean.overall_result)

    return (df_clean, missing_barchart_before, missing_barchart_after)

####################################
# Pieplot
####################################

def plot_pieplot(df):
    y = list(df.overall_result.value_counts().index)
    x = list(df.overall_result.value_counts().values)
    fig_pie = px.pie(df, 
            title='Target distribution',
            values=x, 
            names=y, 
            hole=.3, 
            color_discrete_sequence=px.colors.sequential.Emrld)
    return fig_pie

####################################
# Histogram
####################################
st.cache
def plot_histogram(df):
    numerical_columns = df.select_dtypes("number").columns
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
    return plt

####################################
# Correlation Heatmap
####################################

def plot_corr_heatmap(df):
    numerical_columns = df.select_dtypes("number").columns
    corr_fig = px.imshow(round(df[numerical_columns].corr(),2), 
                        text_auto=True, 
                        aspect="auto", 
                        color_continuous_scale=px.colors.sequential.Emrld)
    return corr_fig

####################################
# Parallel Coordinate Plot
####################################

def plot_para_coordinate(df, plot_options):
    if "overall_number" not in plot_options:
        plot_options.append("overall_number")
    df_fig = df[plot_options]
    parall_fig = px.parallel_coordinates(
                                        df_fig,
                                        color="overall_number", 
                                        color_continuous_scale=px.colors.diverging.Tealrose)
    return parall_fig

####################################
# Scatter Plot
####################################

def plot_scatter(df, x_option, y_option):
    scatter_fig = px.scatter(
                            df, 
                            x=x_option, 
                            y=y_option, 
                            color=df.overall_number, 
                            color_continuous_scale=px.colors.sequential.Emrld
                            )

    scatter_fig.update_layout(
                        {"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"} ,                   
                        xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1),
                        yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1),
                        )
    
    scatter_fig.update_traces(marker=dict(size=20))
    
    return scatter_fig

####################################
# Wordcloud
####################################

def plot_wordcloud(df):
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
    return plt