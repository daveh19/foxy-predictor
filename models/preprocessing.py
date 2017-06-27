
# coding: utf-8

# In[113]:

# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables
from days_to_weeks import week
from pandas import DataFrame
import numpy as np
import pandas as pd
import datetime as dt


# In[120]:

#TODO: add the datum for every week
def average(data, model, weightvector=None):
    '''
    averages over the polling data of all firms according to the data available for each week.
    
    data: polling data and the model that should be used('simple','weightparticipants'or
    'weightfirms'(needs a weightdictionary with a weight for every firm))
    return: dictionary of parties with the average results for every week
    '''
    week_ind={}
    n_weeks = 0
    for key in data:
        wk = week(data[key])
        week_ind[key]= wk
        n_weeks = np.maximum(n_weeks,np.max(wk))
    
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
            result[i,:] /= n      
            
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
    return res

    


# In[115]:

#testing
data = get_tables()


# In[116]:

w = {'allensbach':0.2, 'emnid':0.1, 'forsa':0.1, 'politbarometer':0.1, 'gms':0.2, 'dimap':0.1, 'insa':0.1}


# In[121]:

res = average(data,'weightfirms',w)
print(res)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



