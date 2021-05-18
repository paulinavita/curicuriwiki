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
from sklearn.linear_model import LinearRegression

countries = []

def formatDotAmount(num):
  return float(re.sub(r'[^\w\s.]','',num))

def bsInit(url):
  html = urlopen(url) 
  soup = BeautifulSoup(html, 'html.parser')
  tables = soup.find_all('table')
  return tables

def extractEpidemData():
  tables = bsInit('https://en.wikipedia.org/wiki/Epidemiology_of_schizophrenia')
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
        rates.append(formatDotAmount(rate.text.strip()))

  return ranks, rates

def getEpidemTable(ranks, rates):
  dataFrameEpidem = pd.DataFrame(ranks, index= countries, columns = ['Rank'])
  dataFrameEpidem['DALY rate'] = rates
  dataFrameEpidem.dropna()
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
  df.info()
  print(df.corr())
  df.to_csv('schizo-2.csv')

  # get reg
  getLinearRg()

  # get least square, uncomment if needed
  # getLeastSq()

def getLinearRg():
  data = pd.read_csv('schizo-2.csv') 
  X = data.iloc[:, 1].values.reshape(-1, 1) 
  Y = data.iloc[:, 3].values.reshape(-1, 1)
  linear_regressor = LinearRegression()
  linear_regressor.fit(X, Y)
  Y_pred = linear_regressor.predict(X) 
  sns.scatterplot(x='Rank', y='Sunshine Hours/Year', data=data)
  plt.plot(X, Y_pred, color='red')
  plt.show()

def getLeastSq():
  data = pd.read_csv('schizo-2.csv')
  X = data.iloc[:, 1]
  Y = data.iloc[:, 3]
  plt.scatter(X, Y)
  plt.show()

  X_mean = np.mean(X)
  Y_mean = np.mean(Y)

  num = 0
  den = 0
  for i in range(len(X)):
      num += (X[i] - X_mean)*(Y[i] - Y_mean)
      den += (X[i] - X_mean)**2
  m = num / den
  c = Y_mean - m*X_mean
  
  Y_pred = m*X + c
  plt.scatter(X, Y) # actual
  plt.plot([min(X), max(X)], [min(Y_pred), max(Y_pred)], color='red') # predicted
  plt.show()

getFinalData()
