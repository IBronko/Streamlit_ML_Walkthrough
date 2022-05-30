##########################
# Import libraries/modules
##########################

import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml
from tqdm import tqdm

def app():
    st.title("1. Data Acquisition")

    st.write("This little script demonstrates how to run a Beautifulsoup webscraper to collect data.")

    ##########################################################################
    # Define user header for http request (request might be blocked otherwise)
    ##########################################################################

    headers = {"User-Agent": 
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
            }

    ############################################################################
    # Web-scrape data and create python list of dictionaries for each evaluation
    ############################################################################

    companies = st.multiselect(
        'Select companies',
        ["Adidas", "Bayer", "Delivery-Hero", "Sap", "Mercedes-Benz-Group", "Zalando"],
        ['Adidas'])

    employers = [employer.lower() for employer in companies]

    data = list()
    exceptions_list = list()
    page_count = 2

    with st.spinner('Scraping data...'):
        for employer in tqdm(employers, desc="Scraping data progress"):
            try:
                for i in range(1, page_count, 1):
                    url = f"https://www.kununu.com/de/{employer}/kommentare/{i}"
                    source = requests.get(url, headers=headers).text
                    soup = BeautifulSoup(source, 'lxml')

                    articles = soup.find_all("div", class_="index__reviewBlock__27gnB")

                    for article in articles:
                        sample = {}

                        categories = article.find_all("h4")
                        scores = article.find_all("span", class_="index__stars__2ads4 index__medium__1wpWb index__stars__3lgvx")

                        sample["Employer"] = employer
                        sample["Time"] = article.find("time", class_="p-tiny-regular text-dark-63").text
                        sample["Comment"] = article.find("h3", class_="index__title__2uQec h3-semibold").text
                        sample["Overall"] = article.find("span", class_="p-tiny-bold").text

                        for a, b in zip(reversed(categories), reversed(scores)):
                            sample[a.text] = int(b.attrs["data-score"])

                        data.append(sample)
        
            except Exception as e:
                exception_dict = {}
                exception_dict[employer] = e
                exceptions_list.append(exception_dict) 
                
        if len(exceptions_list) > 0:
            st.error(f"Scraping Errors: {exceptions_list}")

    st.success('Scraping job finished!')

    ################################################################## 
    # Convert list to pandas DataFrame and translate german to english
    ################################################################## 

    if len(data) > 0:

        df = pd.DataFrame(data)

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

        st.write(df)
        st.caption("The result size has been limited to 10 samples per selected company.")

        #################### 
        # Download csv file
        ####################

        def convert_df(df):
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df)

        st.download_button(
            label="Download data as .csv file",
            data=csv,
            file_name='employer_evaluation.csv',
            mime='text/csv',
        )

    else:
        st.write("No data found. Please select at least one company.")