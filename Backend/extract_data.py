"""
module to extract polling data from different sources and return
them in a predefined format to push to the database
"""

import pandas as pd
import io
import requests
from bs4 import BeautifulSoup
import urllib.request

@staticmethod
def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


class Source(object):

    def __init__(self, url):
        self.url = url
        self.date = get_current_timestamp()
        self.page = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.page, 'html.parser')
        self.head = self.soup.find('thead')
        self.body = self.soup.find('tbody')



    def get_table_from_polling_firm(self):
    """
    extracts tables from the website 'http://www.wahlrecht.de/umfragen/'
    for each polling firm, and stores the tables into Pandas dataframes.

    url:    str, the full url of the website,
            e.g. 'http://www.wahlrecht.de/umfragen/emnid.htm'
    Return: Pandas dataframe
    """
    # page = urllib.request.urlopen(url)
    # soup = BeautifulSoup(page, 'html.parser')
    # head = soup.find('thead')
    # body = soup.find('tbody')

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

    def get_tables(self):
        """
        Goes through given url and extracts the tables for all polling firms
        individually, by using get_table_from_polling_firm(arg).

        Return: a dictionary containing the names of polling firms as keywords and the
                pd dataframes as values.
        """

        tables = {}
        # page = urllib.request.urlopen(wahlrecht)
        # soup = BeautifulSoup(page, 'html.parser')

        firms_url = []
        rows = soup.find_all(class_='in')
        for row in rows:
            link = row.find('a')
            firms_url.append(link.get('href'))

        for url in firms_url:
            df = get_table_from_polling_firm(wahlrecht+url)
            tables[url.split('.')[0]] = df

        return tables
