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
import json
from sklearn.linear_model import LinearRegression

countries = []

def formatDotAmount(num):
  return float(re.sub(r'[^\w\s.]','',num))

def splitValue(str):
  return float(str.split(' [')[0])

def bsInit(url):
  html = urlopen(url) 
  soup = BeautifulSoup(html, 'html.parser')
  tables = soup.find_all('table')
  return tables

def extractEpidemData():
  count = 1
  ranks = []
  rates = []
  suicideCountryObj = {}

  with open('./suicide_json.json') as json_file:
    data = json.load(json_file)
    data2 = sorted(data['fact'], key=lambda k: splitValue(k['Value']), reverse=True) 
    # print(type(data2))
    for dataItem in data2:
      # send country list
      countries.append(dataItem['dims']['COUNTRY'])

      ctrName = dataItem['dims']['COUNTRY']
      suicideCountryObj[ctrName] = splitValue(dataItem['Value'])
      rates.append(splitValue(dataItem['Value']))
      ranks.append(count)
      count += 1

  return ranks, rates

def getEpidemTable(ranks, rates):
  dataFrameEpidem = pd.DataFrame(ranks, index= countries, columns = ['Rank'])
  dataFrameEpidem['Suicide Rate'] = rates

  dataFrameEpidem.head(10)
  return dataFrameEpidem


def extractSunData():
  tables = bsInit('https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration')
  countrySunObj = {}

  count = {}
  for table in tables:
    if len(table) >1:
      rows = table.find_all('tr')
      
      for row in rows[1:]:
        cells = row.find_all('td')
        country = cells[0].text.strip()

        if country in countries:
          sun = cells[-2].text.strip()
          sun = formatDotAmount(sun)/10
        
          if country in countrySunObj:
            count[country] += 1
            countrySunObj[country] += sun
          else:
            count[country] = 1
            countrySunObj[country] = sun

  for country in countrySunObj:
    countrySunObj[country] = round(countrySunObj[country]/count[country],2)
  return countrySunObj

# get countries, get rank and rates for first graph
ranks, rates = extractEpidemData()
# dataFrameEpidem = getEpidemTable(ranks, rates)

# get sun rate object for 2nd graph 
countrySunObj = extractSunData()

def handleListCountrySun():
  asc = dict(sorted(countrySunObj.items(), key=lambda item: item[1], reverse=True))
  new_dict = {k: asc[k] for k in set(countries) & set(asc.keys())}
  listed = list(asc.values())
  return listed

def getFinalData():
  df2 = pd.DataFrame.from_dict(countrySunObj, orient='index', columns = ['Sunshine Hours/Year'])
  df = getEpidemTable(ranks, rates).join(df2)
  df.dropna(inplace=True)
  testRegre(ranks[:-64], handleListCountrySun())
  df.info()
  corrMatrix = df.corr()
  sns.heatmap(corrMatrix, annot=True)
  df.to_csv('suicide-and-sun.csv')
  # hehe = sns.scatterplot('Rank', 'Sunshine Hours/Year', data=df)
  # show plot
  plt.show()


def testRegre(x, y):
  xAxis = np.array(x).reshape((-1, 1))
  yAxis = np.array(handleListCountrySun())
  model = LinearRegression().fit(xAxis, yAxis)
  r_sq = model.score(xAxis, yAxis)
  print('coefficient of determination:', r_sq)
  print('intercept:', model.intercept_)
  print('slope:', model.coef_)

getFinalData()
