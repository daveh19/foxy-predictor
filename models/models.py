
# coding: utf-8

# In[6]:

# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
import wahlrecht_polling_firms

import numpy as np
import pandas as pd

data_dict = wahlrecht_polling_firms.get_tables()


# In[7]:

parties = ['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AfD', 'Sonstige']


# In[17]:

def _normalize_to_one(x):
    """Normalize an array so that its sum is 1."""
    return x / np.sum(x)

np.sum(_normalize_to_one(np.linspace(0, 10)))


# In[9]:

def _p2f(x):
    """Convert string with percent to float."""
    return float(x.strip('%').replace(',', '.')) / 100


# In[18]:

def _prediction_to_dataframe(prediction):
    """Wrap an array with the predictions into a dataframe containing the party names."""
    return pd.DataFrame(data=[prediction], columns=parties)

_prediction_to_dataframe(range(len(parties)))


# In[11]:

def average(n_last=5):
    """Average the last `n_last` polls from all polling firms."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(n_last):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].ix[i])))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results
            except ValueError as e:
                print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

average()


# In[12]:

def weighted_average(n_last=5):
    """Average the last `n_last` polls from all polling firms, weighted by the number of participants."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(n_last):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].ix[i])))
                num_people = float(df['Befragte'].ix[i].replace('.', '').replace('T • ', '').replace('O • ', ''))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results * num_people
            except ValueError as e:
                print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

weighted_average()


# In[13]:

def latest():
    """Average the latest polls from all polling firms."""
    return average(n_last=1)

latest()


# In[14]:

def weighted_latest():
    """Average the latest polls from all polling firms, weighted by the number of participants."""
    return weighted_average(n_last=1)

weighted_latest()


# In[15]:

def decay(decay_factor=0.9):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay)."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(len(df)):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].ix[i])))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results * decay_factor**(i+1)
            except ValueError as e:
                print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

decay()


# In[16]:

def weighted_decay(decay_factor=0.9):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay) and each poll is weighted by the number of participants."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(len(df)):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].ix[i])))
                num_people = float(df['Befragte'].ix[i].replace('.', '').replace('T • ', '').replace('O • ', ''))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results * decay_factor**(i+1) * num_people
            except ValueError as e:
                print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

weighted_decay()


# In[ ]:



