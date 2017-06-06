"""
module to extract polling data from different sources and return
them in a predefined format to push to the database
"""
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import datetime
import numpy as np

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
        if page_id not in self.sources.keys():
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



    def get_tables_wahlrecht(self):
        """
        goes through the website 'http://www.wahlrecht.de/umfragen/'
        and extracts the table for all polling firms individually,
        by using get_table_from_polling_firm(arg).

        Return: a dictionary containing the names of polling firms as keywords and the
                pd dataframes as values.
        """
        tables = {}

        firms_url = []
        rows = self.soup.find_all(class_='in')
        for row in rows:
            # print(row)
            link = row.find('a')
            # print(link.get('href'))
            firms_url.append(link.get('href'))

        for url in firms_url:
            key = url.split('.')[0]
            # print(key)
            df = self.get_table_from_polling_firm(self.url + url)
            # df.to_csv('data/' + url.split('.')[0] + '.csv')
            df = self.preprocess(df)
            tables[key] = df

        return tables


    def preprocess(self, table):
        """
        converts the table that consists of strings into a table containing the correct type
        df: pandas dataframe
        return: pandas dataframe
        """
        # drop the column Zeitraum
        table = table.drop('Zeitraum', axis=1)
        # drop the rows containing the true results of the elections
        Idx = np.where(table.Befragte == 'Bundestagswahl')[0]
        Idx = np.append(Idx, np.where(table['CDU/CSU'].str.contains('Umfrage'))[0])
        table = table.drop(Idx)
        table.index = np.arange(table.shape[0])
        # replace the strings %,-
        table = table.replace('%', '', regex=True)
        table = table.replace(',', '.', regex=True)
        table = table.replace('[–?]', '', regex=True)
        # fix the column Befragte !!!!!!!!!!!!!!
        table.Befragte = table.Befragte.replace('[T • ?≈O • ]', '', regex=True)
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
        table.Datum = pd.to_datetime(table.Datum).dt.date
        return table

    def get_table_from_polling_firm(self, url):
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
            header.insert(0, 'Datum')

        df = pd.DataFrame(table, columns=header)
        return df


