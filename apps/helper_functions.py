import streamlit as st
import pandas as pd

def read_file(file):
    df = pd.read_csv(file)
    df = df.sample(frac=1).reset_index()
    df = df.drop("Unnamed: 0", axis=1)
    return df


def basic_cleaning(df, threshold):
    # Rename column labels
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
    # Drop every column with missing values > threshold
    df_missing = df.isna().sum().sort_values(ascending=False)
    drop_list = df_missing[df_missing > threshold].index.to_list()
    df = df.drop(drop_list, axis=1).reset_index(drop=True)
    # Convert float to int
    #float_columns = df.select_dtypes("float64").columns
    #df[float_columns] = df[float_columns].notna().astype("int")
    
    return df

def translate_target(df):
    df = df["overall_result"].replace("Nicht empfohlen", "not_recommended")
    df = df["overall_result"].replace("Empfohlen", "recommended")