"""
Module handling the API endpoint calls to pull data from the database.

getAllParties: returns party names
getPollingData: returns a dictionary of polling data (one dataframe per firm)
"""
import pandas as pd
import datetime


def getAllParties():
    response = pd.read_json('http://localhost:5000/parties/')
    #jsonResponse = json.load(response.decode('utf-8'))
    return response


def correct_date(df):
    '''
    detects pollings with the same date of publication from the same polling firm and
    changes the date of the earlier (least recent) poll to one day further in the past,
    e.g. 2017-03-15 -> 2017-03-14
    df:     pandas DataFrame that contains polls of one polling firm (!)
            and the column 'date'
    return: The same DataFrame without multiple occurence of the same publication date
    '''
    for i in range(len(df) - 1):

        j = i + 1

        if df.iloc[i]['date'] == df.iloc[j]['date']:
            s = df.iloc[j]['date'].split('-')
            new_day = int(s[-1]) - 1
            s_new = s
            s_new[-1] = "%02d" %new_day
            new_date = '-'.join(s_new)
            df.date.iloc[j] = new_date

    return df

def getPollingData(state = False):
    """
    Returns dataframes per firms pulled from the database.
    :param state: If True, returns state data. Else returns federal data. By default False.

    """
    response = pd.read_json('http://localhost:5000/parties/polls')

    df_per_firm = {}
    for i in range(len(response)):
                r = response.ix[[i]]
                df = pd.DataFrame.from_records(r.get('parties')[i])
                if state:
                    df = df[df.region != 'germany'].copy()

                    regions = list(set(df.region))

                    df_corr = []
                    for reg in regions:
                        df_reg = df[df.region == reg].copy()
                        df_corr.append(correct_date(df_reg))
                    df_corr = pd.concat(df_corr, ignore_index=True)
                    date_to_people = {k: v for k, v in zip(df_corr['date'], df_corr['people'])}
                    date_to_region = {k: v for k, v in zip(df_corr['date'], df_corr['region'])}

                else:

                    df_ger = df[df.region == 'germany'].copy()
                    df_corr = correct_date(df_ger)
                    date_to_people = {k: v for k, v in zip(df_corr['date'], df_corr['people'])}
                    date_to_region = {k: v for k, v in zip(df_corr['date'], df_corr['region'])}

                df_p = df_corr.pivot_table(index=['date'], columns=['party_name'], values='percentage')

                ppl = []
                reg = []
                for ind in df_p.index:
                    ppl.append(date_to_people[ind])
                    reg.append(date_to_region[ind])
                df_p['region'] = reg
                df_p['people'] = ppl
                df_p = df_p.sort_index(ascending=False)
                df_per_firm[r['firm'][i]] = df_p

    return df_per_firm
