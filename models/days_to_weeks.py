
# coding: utf-8

# In[24]:

import numpy as np
import pandas as pd
import datetime 
from pandas import DataFrame
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables


# In[29]:

def week(data):
    ''' we want to convert date to weeks,therefore we take the date of the data,
    convert it to days base of the upcoming sundays
    then we convert to week.
    
    data: Pandas dataframe that contains the "Datum" column
    return: the number of the weeks starting from zero for the current week starting from sunday
    
    '''
    X = np.array(pd.to_datetime(data.index).date, dtype=np.datetime64)
    today_date = datetime.date.today()
    next_sunday = np.datetime64(today_date + datetime.timedelta(6 - today_date.weekday()), 'W')
    X = -(X - next_sunday).astype('timedelta64[W]').reshape(-1,1)
    return np.int_(X)#np.int_(X/7)

