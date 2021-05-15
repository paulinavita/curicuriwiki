import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
import re
import matplotlib.pyplot as plt
import seaborn as sns

countries = []

def process_num(num):
  return float(re.sub(r'[^\w\s.]','',num))

def bsInit(url):
  html = urlopen(url) 
  soup = BeautifulSoup(html, 'html.parser')
  tables = soup.find_all('table')
  return tables

def extractEpidemData():
  tables = bsInit('https://en.wikipedia.org/wiki/Epidemiology_of_depression')
  ranks = []
  rates = []

  for table in tables:
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) > 1:
          rank = cells[0]
          ranks.append(int(rank.text))
          
          country = cells[1]
          countries.append(country.text.strip())
          
          rate = cells[2]
          rates.append(process_num(rate.text.strip()))

  return ranks, rates

def getEpidemTable(ranks, rates):
  dataFrameEpidem = pd.DataFrame(ranks, index= countries, columns = ['Rank'])
  dataFrameEpidem['DALY rate'] = rates

  dataFrameEpidem.head(10)
  return dataFrameEpidem

def extractSunData():
  sun_url = urlopen('https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration')
  sun = BeautifulSoup(sun_url, 'html.parser')
  tables = sun.find_all('table')
  country_suns = {}

  count = {}
  for table in tables:
    if len(table) >1:
      rows = table.find_all('tr')
      
      for row in rows[1:]:
        cells = row.find_all('td')
        country = cells[0].text.strip()

        if country in countries:
          sun = cells[-2].text.strip()
          sun = process_num(sun)/10
        
          if country in country_suns:
            count[country] += 1
            country_suns[country] += sun
          else:
            count[country] = 1
            country_suns[country] = sun

  #Find the average temperature of each country
  for country in country_suns:
    # print(country_suns[country],count[country])
    country_suns[country] = round(country_suns[country]/count[country],2)
    # print('Country: {}, Sunshine Hours: {}'.format(country,country_suns[country]))
  return country_suns


ranks, rates = extractEpidemData()
getEpidemTable(ranks, rates)
country_suns = extractSunData()

def getFinalData():
  df2 = pd.DataFrame.from_dict(country_suns, orient='index', columns = ['Sunshine Hours/Year'])
  df = getEpidemTable(ranks, rates).join(df2)
  # df.info()
  df.dropna(inplace=True)
  hehe = sns.scatterplot('Rank', 'Sunshine Hours/Year', data=df)
  plt.show()
  df.corr()
  # df.to_csv('wiki-2.csv')

getFinalData()
