############################## 
# import libraries/modules
############################## 

from employers import employers

from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml
from tqdm import tqdm

########################################################################################## 
# define user header for http request (request might be blocked otherwise)
##########################################################################################

headers = {"User-Agent": 
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
          }

########################################################################################## 
# web-scrape data and create python list of dictionaries for each evaluation
##########################################################################################

data = list()
exceptions_list = list()
page_count = 10

for employer in tqdm(employers, desc="Scraping data progress"):
    try:
        for i in range(page_count):
            url = f"https://www.kununu.com/de/{employer}/kommentare/{i}"
            source = requests.get(url, headers=headers).text
            soup = BeautifulSoup(source, 'lxml')

            articles = soup.find_all("div", class_="index__reviewBlock__27gnB")

            for article in articles:
                sample = {}

                #print(employer)
                #print(article.find("time", class_="p-tiny-regular text-dark-63").text)
                #print(article.find("h3", class_="index__title__2uQec h3-semibold").text)
                #print(article.find("span", class_="p-tiny-bold").text)

                categories = article.find_all("h4")
                scores = article.find_all("span", class_="index__stars__2ads4 index__medium__1wpWb index__stars__3lgvx")

                sample["Employer"] = employer
                sample["Time"] = article.find("time", class_="p-tiny-regular text-dark-63").text
                sample["Comment"] = article.find("h3", class_="index__title__2uQec h3-semibold").text
                sample["Overall"] = article.find("span", class_="p-tiny-bold").text

                for a, b in zip(reversed(categories), reversed(scores)):
                    #print(a.text, ":", b.attrs["data-score"])
                    sample[a.text] = int(b.attrs["data-score"])

                data.append(sample)
  
    except Exception as e:
        exception_dict = {}
        exception_dict[employer] = e
        exceptions_list.append(exception_dict) 
        
print(f"Errors: {exceptions_list}")

############################################################ 
# convert list to pandas DataFrame and save as .csv file
############################################################ 

df = pd.DataFrame(data)
df.to_csv("kununu_data.csv")