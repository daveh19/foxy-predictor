
# coding: utf-8

# In[1]:

# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
import wahlrecht_polling_firms

import numpy as np
import pandas as pd

data_dict = wahlrecht_polling_firms.get_tables()


# In[2]:

parties = ['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AfD', 'Sonstige']


# In[3]:

def _normalize_to_one(x):
    """Normalize an array so that its sum is 1."""
    return x / np.sum(x)

np.sum(_normalize_to_one(np.linspace(0, 10)))


# In[4]:

def _p2f(x):
    """Convert string with percent to float."""
    return float(x.strip('%').replace(',', '.')) / 100


# In[5]:

def _prediction_to_dataframe(prediction):
    """Wrap an array with the predictions into a dataframe containing the party names."""
    return pd.DataFrame(data=[prediction], columns=parties)

_prediction_to_dataframe(range(len(parties)))


# In[6]:

# TODO: Default parameter values for data_dict and model in the functions below are just here for backwards compatibility.
# Remove them once the frontend is only calling apply.


# In[7]:

def average(data_dict=data_dict, n_last=5):
    """Average the last `n_last` polls from all polling firms."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(min(n_last, len(df))):  # do not use more rows than the dataframe has
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].iloc[i])))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results
            except ValueError as e:
                pass
                #print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

average(data_dict)


# In[8]:

def weighted_average(data_dict=data_dict, n_last=5):
    """Average the last `n_last` polls from all polling firms, weighted by the number of participants."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(min(n_last, len(df))):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].iloc[i])))
                num_people = float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', ''))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results * num_people
            except ValueError as e:
                pass
                #print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

weighted_average(data_dict)


# In[9]:

def latest(data_dict=data_dict):
    """Average the latest polls from all polling firms."""
    return average(data_dict, n_last=1)

latest(data_dict)


# In[10]:

def weighted_latest(data_dict=data_dict):
    """Average the latest polls from all polling firms, weighted by the number of participants."""
    return weighted_average(data_dict, n_last=1)

weighted_latest(data_dict)


# In[11]:

def decay(data_dict=data_dict, decay_factor=0.9):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay)."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(len(df)):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].iloc[i])))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results * decay_factor**(i+1)
            except ValueError as e:
                pass
                #print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

decay(data_dict)


# In[12]:

def weighted_decay(data_dict=data_dict, decay_factor=0.9):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay) and each poll is weighted by the number of participants."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(len(df)):
            # TODO: Contains some fixes to convert strings to floats. Do this in the data already.
            try:
                results = np.array(list(map(_p2f, df[parties].iloc[i])))
                num_people = float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', ''))
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results * decay_factor**(i+1) * num_people
            except ValueError as e:
                pass
                #print(e)  # TODO: Probably just a conversion error. Remove this once the data is fixed.
    return _prediction_to_dataframe(_normalize_to_one(prediction))

weighted_decay(data_dict)


# In[13]:

def apply_model(data_dict=data_dict, model=average, **kwargs):
    """Make a prediction using `model` for each time point in the data."""
    num_timesteps = max([len(df) for df in data_dict.values()])  # take the max from all dataframes
    print('Applying model to {} time points...'.format(num_timesteps))
    
    prediction_df = model(data_dict, **kwargs)
    
    for i in range(1, num_timesteps):
        sliced_data_dict = {key: df[i:] for key, df in data_dict.items()}
        # TODO: Appending the dataframes is probably not very efficient.
        # TODO: Due to ill-formated data, the resulting dataframe contains NaNs sometimes.
        prediction_df = prediction_df.append(model(sliced_data_dict, **kwargs), ignore_index=True)
        
    return prediction_df
    
#pd.options.display.max_rows = 300
#apply_model(data_dict, average)


# In[14]:

def score_model(data_dict, model, **kwargs):
    prediction_df = apply_model(data_dict, model, **kwargs)
    # TODO: Compute average of all dataframes in data_dict, then calculate MSE between this average and the predictions.
    return 0

#score_model(data_dict, average)


# In[15]:

models = [average, weighted_average, latest, weighted_latest, decay, weighted_decay]
def test_all_models():
    print('Testing all models with default parameters...')
    for model in models:
        mse = score_model(data_dict, model)
        print('MSE for model "{}": {}'.format(model.__name__, mse))
        
#test_all_models()


# In[16]:

#import matplotlib.pyplot as plt
#%matplotlib inline

#for model in models:
#    prediction_df = apply_model(data_dict, model)
#    plt.plot(prediction_df['CDU/CSU'], label=model.__name__)
#    plt.legend()
#        #print('MSE for model "{}": {}'.format(model.__name__, mse))


# In[ ]:



