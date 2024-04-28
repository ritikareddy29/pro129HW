from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

dwarf_star_data = []

def scrape_more_data(hyperlink):
    #print(hyperlink)
    
    ## ADD CODE HERE ##
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class" : "value"})[0].contents[0])
                except:
                    temp_list.append("")
        dwarf_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


dwarf_star_data = pd.read_csv("updated_scraped_data.csv")


print(dwarf_star_data[0:10])

# Remove '\n' character from the scraped data
scraped_data = []

for row in dwarf_star_data:
    replaced = []
    ## ADD CODE HERE ##
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)
    scraped_data.append(replaced)

print(scraped_data)

headers = ["star_name","distance_data", "mass", "radius"]

new_star_df_1 = pd.DataFrame(scraped_data,columns = headers)

new_star_df_1.dropna(inplace=True)

new_star_df_1['radius'] = new_star_df_1['radius'] * 0.102763
new_star_df_1['mass'] = new_star_df_1['mass'] * 0.000954588


# Convert to CSV
new_star_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")

merge_stars_df = pd.merge(star_df_1, new_star_df_1, on="id" )
merge_planets_df.to_csv('merge.planets.csv')