
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request


# In[263]:

def janitor(table):
    """
    cleans a single table extracted for the states
    """
    # drop rows containing only NaNs/None
    table = table.dropna(axis=0, how='all')

    # replace all empty entries with NaN
    table = table.replace('', 'NaN', regex=True)

    table.index = np.arange(table.shape[0])

    # drop the rows containing the true results of the elections
    Idx = np.where(table['Institut(Datum)'].str.contains('Bundestagswahl'))
    table = table.drop(Idx[0])
    table.index = np.arange(table.shape[0])

    # split 'BefrateZeitraum' into two columns
    for i, n in enumerate(table['BefragteZeitraum']):
        if pd.isnull(n):
            table['BefragteZeitraum'][i] = np.nan
        elif len(n) >= 13:
            n = n.split('\n', 1)[0]
            table['BefragteZeitraum'][i] = n[:-13]
    table.rename(columns={'BefragteZeitraum': 'Befragte'}, inplace=True)

    # split the column 'Institut(Datum)' into two columnbs
    institut_datum = table['Institut(Datum)'].str.extract('([A-z]+)?([(])?(\d+.\d+.\d+)', expand=False)
    institut_datum = institut_datum.drop(1, axis=1)
    institut_datum.columns = ['Institut', 'Datum']
    table = pd.concat([institut_datum, table.iloc[:,1:]], axis=1)

    # convert the date to type date
    table.Datum = table.Datum.apply(lambda cell: pd.to_datetime(cell, format='%d.%m.%Y')
                                      if len(cell)==10 
                                      else pd.to_datetime(cell, format='%d.%m.%y'))
    if not table.empty:
        table.Datum = table.Datum.dt.date

    # replace the strings %,-
    table = table.replace(',', '.', regex=True)
    table = table.replace('[–?%)≈/*]', '', regex=True)
    table = table.replace('T • ', '', regex=True)
    table = table.replace('O • ', '', regex=True)

    # extract the AfD from Sonstige
    AfD = table.Sonstige.str.extract('(AfD \d+)', expand=False)
    AfD = AfD.str.extract('(\d+)', expand=False)
    table.insert(9, 'AfD', AfD)

    # combine remaining percentages in Sonstige
    Sonst = table.Sonstige.replace('(AfD \d+)', '', regex=True)
    Sonst = Sonst.str.findall('(\d+)')
    table.Sonstige = Sonst.apply(lambda cell: np.array(cell).astype(float).sum() if cell!=[] else np.nan)

    # convert all numbers to float
    table = table.replace('', np.nan, regex=True)
    table[table.keys()[3:]] = table[table.keys()[3:]].astype(float)
    
    return table


# In[271]:

def get_states_tables():
    """
    Goes through the website 'http://www.wahlrecht.de/umfragen/laender.htm'
    and extracts the table for states individually, 
    
    Return: a dictionary containing the id names of the states as keywords and the 
            pd dataframes as values.
    """
    tables = {} # {'state': df}

    page = urllib.request.urlopen('http://www.wahlrecht.de/umfragen/laender.htm')
    soup = BeautifulSoup(page, 'html.parser')
    
    # Find the subtables
    states = soup.find_all('th', colspan='10', id=True)
    rows = soup.find_all('tr')
    header = [col.get_text() for col in soup.find_all('th', class_=True, limit=9)]
    
    # Initialize with empty/unimportant values
    table = [] # df
    new_table = pd.DataFrame()
    name = "ignore"
    for row in rows:
        # Start point of a new state
        if row.find('th', colspan='10', id=True) != None:
            table = []
            name = row.contents[1].get('id')

        # Read the data of the subtable
        cols = row.find_all('td', rowspan=False)
        cols = [ele.text.strip() for ele in cols]
        table.append([ele if ele else None for ele in cols])
        
        # End point for each state
        if row.find('th', colspan='10', class_="trenner") != None: 
            # Don't use the information outside the states.
            if name != 'ignore':
                try:
                    tables[name] = pd.DataFrame(table, columns=header)
                except AssertionError:
                    tables[name] = pd.DataFrame(columns=header)

    # Add last table, that doesn't have trenner at the end
    tables[name] = pd.DataFrame(table, columns=header)

    return tables


# In[272]:

def get_tables():
    """
    extracts the tables from 'http://www.wahlrecht.de/umfragen/laender.htm',
    cleans the tables,
    returns a dictionary containing the abbreviations of the states as keywords
    and the corresponding tables as values.
    """
    states = get_states_tables()
    for state, table in states.items():
        states[state] = janitor(table)
    return states


# In[274]:

# tables = get_tables()
# table = tables['th']


# In[ ]:



