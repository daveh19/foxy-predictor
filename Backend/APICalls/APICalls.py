import json
import pandas as pd

def getAllParties():
    response = pd.read_json('http://localhost:5000/parties/')
    #jsonResponse = json.load(response.decode('utf-8'))
    return response

def getPollingData():
    response = pd.read_json('http://localhost:5000/parties/polls')
    df_per_firm = {}
    for i in range(len(response)):
        r = response.ix[[i]]
        df = pd.DataFrame.from_records(r.get('parties')[i])
        df_p = df.pivot_table(index=['date'], columns='party_name', values='percentage')
        date_to_people = {k:v for k,v in zip(df['date'],df['people'])}
        ppl = []
        for ind in df_p.index:
            ppl.append(date_to_people[ind])
        df_p['people'] = ppl
        df_p = df_p.sort_index(ascending=False)
        df_per_firm[r['firm'][i]] = df_p
    return df_per_firm
