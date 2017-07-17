
# coding: utf-8

# In[1]:

"""
This script extracts tables from the website 'http://www.wahlrecht.de/umfragen/' 
for each polling firm individually.

Call the function get_tables() will return a dictionary containing the firm names 
as keywords and corresponding Pandas dataframe as values.
"""


# In[1]:

import numpy as np
import pandas as pd
import io
import requests
from bs4 import BeautifulSoup
import urllib.request

wahlrecht = 'http://www.wahlrecht.de/umfragen/'


# In[2]:

def get_table_from_polling_firm(url):
    """
    extracts tables from the website 'http://www.wahlrecht.de/umfragen/'
    for each polling firm, and stores the tables into Pandas dataframes.
    
    url:    str, the full url of the website, 
            e.g. 'http://www.wahlrecht.de/umfragen/emnid.htm'
    Return: Pandas dataframe
    """
    
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    head = soup.find('thead')
    body = soup.find('tbody')

    table = []
    rows = body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        table.append([ele if ele else np.nan for ele in cols]) 

    header = []
    cols = head.find_all('th')
    for col in cols:
        if col.get_text() != '\xa0':
            header.append(col.get_text())
    if header.count('Datum') == 0:
        header.insert(0, 'Datum')

    df = pd.DataFrame(table).dropna(how='all',axis=1)
    df.columns = header
    return df


# In[12]:

def preprocess(table):
    """
    converts the table that consists of strings into a table containing the correct type
    df: pandas dataframe 
    return: pandas dataframe 
    """
    # drop the column Zeitraum
    table = table.drop('Zeitraum', axis=1)
    # drop the rows containing the true results of the elections
    Idx = np.where(table.Befragte=='Bundestagswahl')[0]
    Idx = np.append(Idx, np.where(table['CDU/CSU'].str.contains('Umfrage'))[0])
    table = table.drop(Idx)
    table.index = np.arange(table.shape[0])
    # replace the strings %,-
    table = table.replace('%', '', regex=True)
    table = table.replace(',', '.', regex=True)
    table = table.replace('[–?]', '', regex=True)
    # fix the column Befragte !!!!!!!!!!!!!!
    table.Befragte = table.Befragte.replace('[T • ?≈O • .]', '', regex=True)
    # replace all empty entries with NaN
    table = table.replace('', 'NaN', regex=True)

    # if the colomn Sonstige contains entries with more than one number
    try: 
        table.Sonstige = table.Sonstige.astype(float)
    except ValueError:
        for i, n in enumerate(table.Sonstige):
            if len(n) > 2:
                digits = np.array([digit for digit in np.arange(10).astype(str) if digit in n])
                table.Sonstige[i] = digits.astype(int).sum()
                table.Sonstige = table.Sonstige.astype(float)

    # convert all numbers to float
    table[table.keys()[1:]] = table[table.keys()[1:]].astype(float)
    # convert the date to type date
    table.Datum = pd.to_datetime(table.Datum, format='%d.%m.%Y').dt.date
    return table


# In[13]:

def get_tables():
    """
    goes through the website 'http://www.wahlrecht.de/umfragen/'
    and extracts the table for all polling firms individually, 
    by using get_table_from_polling_firm(arg).
    
    Return: a dictionary containing the names of polling firms as keywords and the 
            pd dataframes as values.
    """
    
    tables = {}
    
    page = urllib.request.urlopen(wahlrecht)
    soup = BeautifulSoup(page, 'html.parser')

    firms_url = []
    rows = soup.find_all(class_='in')
    for row in rows:
        #print(row)
        link = row.find('a')
        #print(link.get('href'))
        firms_url.append(link.get('href'))

    for url in firms_url:
        key = url.split('.')[0]
        #print(key)
        df = get_table_from_polling_firm(wahlrecht+url)
        #df.to_csv('data/' + url.split('.')[0] + '.csv')
        df = preprocess(df)
        tables[key] = df
    
    return tables



