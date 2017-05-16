
# coding: utf-8

# In[ ]:

"""
This script extracts tables from the website 'http://www.wahlrecht.de/umfragen/' 
for each polling firm individually.

Call the function get_tables() will return a dictionary containing the firm names 
as keywords and corresponding Pandas dataframe as values.
"""


# In[1]:

import pandas as pd
import io
import requests
from bs4 import BeautifulSoup
import urllib.request

wahlrecht = 'http://www.wahlrecht.de/umfragen/'


# In[21]:

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
        table.append([ele for ele in cols if ele]) 

    header = []
    cols = head.find_all('th')
    for col in cols:
        if col.get_text() != '\xa0':
            header.append(col.get_text())
    if header.count('Datum') == 0:
        header.insert(0, 'Date')

    df = pd.DataFrame(table, columns=header)
    return df


# In[53]:

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
        df = get_table_from_polling_firm(wahlrecht+url)
        #df.to_csv('data/' + url.split('.')[0] + '.csv')
        tables[url.split('.')[0]] = df
    
    return tables


# In[59]:

tables = get_tables()


# In[60]:

tables.keys()


# In[ ]:




# In[23]:

""" 
#this is a not nested version of the function get_table_from_polling_firm for testing purpose

url = firms_url[-1] 
#df = get_table_from_polling_firm(wahlrecht+url)

page = urllib.request.urlopen(wahlrecht + url)
soup = BeautifulSoup(page, 'html.parser')

head = soup.find('thead')
body = soup.find('tbody')

table = []
rows = body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    table.append([ele for ele in cols if ele]) 

header = []
cols = head.find_all('th')
for col in cols:
    if col.get_text() != '\xa0':
        header.append(col.get_text())
if header.count('Datum') == 0:
    header.insert(0, 'Date')

df1 = pd.DataFrame(table, columns=header)
"""


# In[ ]:




# In[ ]:



