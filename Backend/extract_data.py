"""
Module for scraping the webpages containing our data sources
Pulls polling data from different sources and return them in a predefined format to push to the database.
Sources: Source object's class attribute 'sources'.
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

    sources = {'wahlrecht_country': 'http://www.wahlrecht.de/umfragen/',
               'wahlrecht_states': 'http://www.wahlrecht.de/umfragen/laender.htm'}

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
        if self.page_id == 'wahlrecht_country':
            tables = self.get_tables_wahlrecht_country()
        if self.page_id == 'wahlrecht_states':
            tables = self.get_tables_wahlrecht_states()

        return tables

    def get_tables_wahlrecht_country(self):
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
            df = self.get_table_from_polling_firm_country(self.url + url)
            # df.to_csv('data/' + url.split('.')[0] + '.csv')
            df = self.preprocess_country(df)
            tables[key] = df

        return tables

    def get_tables_wahlrecht_states(self):
        """
        goes through the website 'http://www.wahlrecht.de/umfragen/'
        and extracts the table for all polling firms individually,
        by using get_table_from_polling_firm(arg).

        Return: a dictionary containing the names of polling firms as keywords and the
                pd dataframes as values.
        """
        states = self.get_table_from_polling_firm_states()
        for state, table in states.items():
            states[state] = self.preprocess_states(table)
        return states

    def preprocess_states(self, table):
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
        table = pd.concat([institut_datum, table.iloc[:, 1:]], axis=1)

        # convert the date to type date
        table.Datum = table.Datum.apply(lambda cell: pd.to_datetime(cell, format='%d.%m.%Y')
        if len(cell) == 10
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
        table.Sonstige = Sonst.apply(lambda cell: np.array(cell).astype(float).sum() if cell != [] else np.nan)

        # convert all numbers to float
        table = table.replace('', np.nan, regex=True)
        table[table.keys()[3:]] = table[table.keys()[3:]].astype(float)
        table['Befragte'] = table['Befragte'].astype(int)

        return table

    def preprocess_country(self, table):
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
        #TODO: the following line provokes an error on my system (DH)
        table['Befragte'] = table['Befragte'].astype(int)
        # convert the date to type date
        table.Datum = pd.to_datetime(table.Datum).dt.date
        return table

    def get_table_from_polling_firm_country(self, url):
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

        df = pd.DataFrame(table).dropna(how='all', axis=1)
        df.columns = header
        return df

    def get_table_from_polling_firm_states(self):
        """
        Goes through the website 'http://www.wahlrecht.de/umfragen/laender.htm'
        and extracts the table for states individually,

        Return: a dictionary containing the id names of the states as keywords and the
                pd dataframes as values.
        """
        tables = {}  # {'state': df}

        page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(page, 'html.parser')

        # Find the subtables
        states = soup.find_all('th', colspan='10', id=True)
        rows = soup.find_all('tr')
        header = [col.get_text() for col in soup.find_all('th', class_=True, limit=9)]

        # Initialize with empty/unimportant values
        table = []  # df
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
