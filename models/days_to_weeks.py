
# coding: utf-8

# In[2]:

import numpy as np
import pandas as pd
import datetime as dt
from pandas import DataFrame
# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables


#Y = data[['CDU/CSU','SPD','Linke','Grüne','FDP','AfD']]


#times=np.arange(len(Y['CDU/CSU']))

#X = times.reshape(-1, 1)


# In[3]:

data=get_tables()


# In[9]:

allensbach_data=data['allensbach']
allensbach_data


# In[18]:

def week(data):
    X = pd.to_datetime(data.Datum)
    X=-(X-data.Datum.iget(0)).astype('timedelta64[D]').reshape(-1,1)
    return np.int_(X/7)


# In[19]:

week(allensbach_data)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



