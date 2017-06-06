"""
module to extract polling data from different sources and return
them in a predefined format to push to the database
"""
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import datetime


def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class Source(object):
    """
    Initializes a Source object to load tables from webpages.

    sources : dict storing all pages and corresponding urls

    Args:
        page_id: identifier for different sources
    """

    sources = {'wahlrecht': 'http://www.wahlrecht.de/umfragen/'}

    def __init__(self, page_id):
        self.page_id = page_id
        if page_id not in self.source.keys():
            raise ValueError("The page_id {} is not valid!".format(self.page_id))
        else:
            self.url = self.sources[self.page_id]
        self.date = get_current_timestamp()
        self.page = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.page, 'html.parser')

    def get_tables(self):
        """
        Method that returns tables. Calls the method respectively to page_id.
        """

        if self.page_id == 'wahlrecht':
            tables = self.get_tables_wahlrecht()

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
        rows = self.soup.find_all(class_='in')
        for row in rows:
            link = row.find('a')
            firms_url.append(link.get('href'))

        for url in firms_url:
            df = self.get_table_from_polling_firm(self.url + url)
            tables[url.split('.')[0]] = df

        return tables
