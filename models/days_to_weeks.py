
# coding: utf-8

# In[8]:

import numpy as np
import pandas as pd
import datetime as dt
from pandas import DataFrame
# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables
data=pd.read_excel('C:/Users/neg/Predictor/models/Multi_dimentional_data_covar/01_Projektion.xlsx',skiprows=7).dropna(axis=1,how='all')

data = data[['Datum','CDU/CSU','SPD','Linke','Grüne','FDP','AfD']].dropna()

#Y = data[['CDU/CSU','SPD','Linke','Grüne','FDP','AfD']]

def week(data):
    df = pd.DataFrame(data)
    X = pd.to_datetime(data.Datum)
    X=-(X-df['Datum'].iget(0)).astype('timedelta64[D]').reshape(-1,1)
    return np.int_(X/7)
#times=np.arange(len(Y['CDU/CSU']))

#X = times.reshape(-1, 1)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



