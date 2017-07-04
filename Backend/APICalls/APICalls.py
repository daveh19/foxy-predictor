import json
import pandas as pd

def getAllParties():
    response = pd.read_json('http://localhost:5000/parties/')
    #jsonResponse = json.load(response.decode('utf-8'))
    return response

def getPollingData(state = False):
    """
    Returns dataframes per firms pulled from the database.
    :param state: If True, returns state data. Else returns federal data. By default False.

    """
    response = pd.read_json('http://127.0.0.1:5000/parties/polls')

    df_per_firm = {}
    for i in range(len(response)):
                r = response.ix[[i]]
                df = pd.DataFrame.from_records(r.get('parties')[i])
                df_p = df.pivot_table(index=['date'], columns='party_name', values='percentage')
                date_to_people = {k: v for k, v in zip(df['date'], df['people'])}
                date_to_region = {k: v for k, v in zip(df['date'], df['region'])}
                ppl = []
                reg = []
                for ind in df_p.index:
                    ppl.append(date_to_people[ind])
                    reg.append(date_to_region[ind])
                df_p['region'] = reg
                df_p['people'] = ppl
                df_p = df_p.sort_index(ascending=False)
                if state:
                    df_per_firm[r['firm'][i]] = df_p[df_p['region'] != 'germany']
                else:
                    df_per_firm[r['firm'][i]] = df_p[df_p['region'] == 'germany']
                # f_per_firm[r['firm'][i]] = df_p
    return df_per_firm
