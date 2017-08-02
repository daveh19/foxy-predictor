# Contains:
#       str_to_int_arr
#       average

# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
#CONSIDER: can I just comment out the following lines? We should be using the server.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables

from days_to_weeks import week
from pandas import DataFrame
import numpy as np
import pandas as pd
import datetime as dt

def str_to_int_arr(arr, ind, name = 'Befragte'):
    """
    arr: Series object of a dataframe column - for people/befragte
    output:
    integers in correct format
    """
    ppl = np.array(arr, dtype = np.float)
    # ppl = [n(p) if p is not None else np.nan for p in ppl]
    ppl = [round(p*1e3) if p < 10 else round(p) for p in ppl]
    ppl = [int(p) if not np.isnan(p) else None for p in ppl]
    return pd.Series(ppl, index=ind, name = name)

#TODO: add the datum for every week
def average(data, model = 'weightparticipants', weightvector=None):
    '''
    averages over the polling data of all firms according to the data available for each week.

    data: polling data and the model that should be used('simple','weightparticipants'or
    'weightfirms'(needs a weightdictionary with a weight for every firm))
    return: dictionary of parties with the average results for every week
    '''
    week_ind={}
    n_weeks = 0
    to_drop=[]
    for key in data:
        data[key] = data[key].rename(index=str, columns={"people": "Befragte"})
        ind = data[key]['Befragte'].index
        data[key]['Befragte'] = str_to_int_arr(data[key]['Befragte'], ind, name='Befragte')

        if len(data[key].index) ==0 :
            to_drop.append(key)
            continue

        wk = week(data[key])
        week_ind[key]= wk
        n_weeks = np.maximum(n_weeks,np.max(wk))
    [data.pop(key,None) for key in to_drop]
    n_parties=7
    result=np.zeros((n_weeks,n_parties))
    total_part = np.zeros(n_weeks)
    parties=['CDU/CSU','SPD','GRÜNE','FDP','LINKE','AfD','Sonstige']


    if model == 'simple':
        for i in np.arange (n_weeks):
            n = 0
            for key in data:
                if i in week_ind[key]:
                    current_ind = np.where(week_ind[key]==i)[0][0]
                    total_part[i] += data[key]['Befragte'][current_ind]
                    j = 0
                    for p in parties:
                        result[i,j] += data[key][p][current_ind]
                        j += 1
                    n += 1
            result[i,:] /= n

    if model == 'weightparticipants':
        for i in np.arange(n_weeks):
            n = 0
            for key in data:
                if i in week_ind[key]:
                    current_ind = np.where(week_ind[key]==i)[0][0]
                    total_part[i] += data[key]['Befragte'][current_ind]
                    n_part = data[key]['Befragte'][current_ind]
                    j = 0
                    for p in parties:
                        result[i,j] += data[key][p][current_ind]*n_part
                        j += 1
                    n += n_part
            #TODO: runtime error on following line
            #   'invalid value encountered in true_divide'
            # probably a divide by zero issue. YES
            if n > 0:
                result[i,:] /= n
            else:
                #import pdb; pdb.set_trace()
                print('Divide by zero avoided! - in weightparticipants section of preprocessing average() function')

    if model == 'weightfirms':
        for i in np.arange(n_weeks):
            n = 0
            for key in data:
                if i in week_ind[key]:
                    current_ind = np.where(week_ind[key]==i)[0][0]
                    total_part[i] += data[key]['Befragte'][current_ind]
                    j = 0
                    for p in parties:
                        result[i,j] += data[key][p][current_ind]*weightvector[key]
                        j += 1
                    n += weightvector[key]
            result[i,:] /= n

    res_dict = {}
    j = 0
    for p in parties:
        res_dict[p] = result[:,j]
        j += 1
    res = pd.DataFrame.from_dict(res_dict)
    today_date = dt.date.today()
    next_sunday = today_date + dt.timedelta(6 - today_date.weekday())
    sundays = np.array(np.zeros(n_weeks),dtype='datetime64[ms]')
    for i in np.arange(n_weeks):
        sundays[i] = np.array(next_sunday-dt.timedelta(np.float64(7*i)),dtype='datetime64[ms]')

    res['Befragte'] = total_part
    res['Datum'] = sundays
    while res.loc[0]['Befragte'] == 0:
        res  = res.drop(0,axis=0)
        res.index = res.index-1
    return res
