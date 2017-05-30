"""
module to extract polling data from different sources and return
them in a predefined format to push to the database
"""

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


class Source(object):
    """
    Initializes a Source object to load tables from webpages.
    Args:
        url: url to pull data from
        # page_id: name of the webpage, eg. for
    """
    def __init__(self, url, page_id = 'wahlrecht'):
        self.url = url
        self.page_id = page_id
        self.date = get_current_timestamp()
        self.page = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.page, 'html.parser')

    def get_table(self):
        """
        Method that returns tables. Calls the method respectively to page_id.
        """

        if page_id == 'wahlrecht':
            tables = get_tables_wahlrecht(self.url)
        return tables

    def get_table_from_polling_firm(self, sub_url):
        """
        extracts tables from the website 'http://www.wahlrecht.de/umfragen/'
        for each polling firm, and stores the tables into Pandas dataframes.

        url:    str, the full url of the website,
                e.g. 'http://www.wahlrecht.de/umfragen/emnid.htm'
        Return: Pandas dataframe
        """
        page = urllib.request.urlopen(sub_url)
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

    def get_tables_wahlrecht(self):
        """
        Goes through given url and extracts the tables for all polling firms
        individually, by using get_table_from_polling_firm(arg).

        Return: a dictionary containing the names of polling firms as keywords and the
                pd dataframes as values.
        """
        tables = {}
        firms_url = []
        rows = soup.find_all(class_='in')
        for row in rows:
            link = row.find('a')
            firms_url.append(link.get('href'))

        for url in firms_url:
            df = get_table_from_polling_firm(self.url + url)
            tables[url.split('.')[0]] = df

        return tables
