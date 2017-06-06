
# coding: utf-8

# # Model framework

# In[1]:

# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
import wahlrecht_polling_firms

import numpy as np
import pandas as pd


# ## Data & Helper functions

# In[2]:

parties = ['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AfD', 'Sonstige']


# In[3]:

# TODO: Maybe rename to complete_data_dict or full_data_dict to distinguish it from keyword args.
data_dict = wahlrecht_polling_firms.get_tables()

def _preprocess_df(df):
    df = df.fillna(0)  # TODO: Some values are NaN --> how to handle these? Especially, the numbers have to add up to 1.
    df['Befragte'] = df['Befragte'].apply(lambda x: int(x.replace('.', '').replace('NaN', '0')))  # TODO: Befragte column is string so far. Sometimes, there are also NaN values --> how to handle these? Should the polls be ignored for weighting or should an "average" value be used?
    #df[parties] /= 100  # TODO: Have values as 37 or 0.37?
    return df

#data_dict = {key: _preprocess_df(df) for key, df in data_dict.items()}


# In[4]:

def _normalize_to_hundred(x):
    """Normalize an array so that its sum is 1."""
    return 100 * x / np.sum(x)

np.sum(_normalize_to_hundred(np.linspace(0, 10)))


# In[5]:

def _prediction_to_dataframe(prediction):
    """Wrap an array with the predictions into a dataframe containing the party names."""
    return pd.DataFrame(data=[prediction], columns=parties)

_prediction_to_dataframe(range(len(parties)))


# In[6]:

def mse(poll_df, prediction_df):
    """Calculate the mean squared error between the polling results in `poll_df` and the predictions in `prediction_df`. Average over all parties."""
    # TODO: Have data_dict as parameter here? Or hand over data_dict['allensbach'] directly?
    # TODO: Refactor this once the model is wrapped in a class.
    mse = 0
    for party in parties:
        true_results = poll_df[party]
        predicted_results = prediction_df[party][1:1+len(true_results)]  # first point is prediction into the future, do not use it
        mse += np.mean((true_results - predicted_results)**2)
    return mse / len(parties)


# ## Models

# In[7]:

class Model():

    def fit(self, data_dict=data_dict):
        """Optional fit step to call before predictions. Leave empty if the model does not support fitting."""
        return

    def predict(self, data_dict=data_dict):
        raise NotImplementedError()

    def predict_all(self, data_dict=data_dict):
        """Make a prediction for each time point in the data."""
        num_timesteps = max([len(df) for df in data_dict.values()])  # take the max from all dataframes
        #print('Applying model to {} time points...'.format(num_timesteps))

        # First prediction, append the other ones below.
        prediction_df = self.predict(data_dict)

        for i in range(1, num_timesteps):
            sliced_data_dict = {key: df[i:] for key, df in data_dict.items()}
            # TODO: Maybe speed up models, especially the decay models.
            # Note: Appending the data frames takes up almost no time here, the bottleneck is the model.
            # TODO: Due to ill-formated data, the resulting dataframe contains NaNs sometimes.
            prediction_df = prediction_df.append(self.predict(sliced_data_dict), ignore_index=True)

        return prediction_df

    def score(self, data_dict=data_dict, polling_firm=None):
        """Calculate a score for the model (lower is better). The score is the mean squared error between the model's predictions and the true results.
        If `polling_firm` is None (default), return a dict with the score for each polling firm. Otherwise, return only the score for that polling firm."""
        prediction_df = self.predict_all(data_dict)

        if polling_firm is None:
            return {polling_firm: mse(poll_df, prediction_df) for polling_firm, poll_df in data_dict.items()}
        else:
            return mse(data_dict[polling_firm], prediction_df)


# In[8]:

def average(data_dict=data_dict, n_last=5):
    """Average the last `n_last` polls from all polling firms."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(min(n_last, len(df))):  # do not use more rows than the dataframe has
            results = df[parties].iloc[i]
            # TODO: Polls from different polling firms have different time spacing. Take this into account.
            prediction += results
    return _prediction_to_dataframe(_normalize_to_hundred(prediction))

average(data_dict)


# In[9]:

class AverageModel(Model):
    """Average the last `n_last` polls from all polling firms."""

    def __init__(self, n_last=5):
        self.n_last = n_last

    def predict(self, data_dict=data_dict):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(min(self.n_last, len(df))):  # do not use more rows than the dataframe has
                results = df[parties].iloc[i]
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))

AverageModel().predict(data_dict)


# In[10]:

def weighted_average(data_dict=data_dict, n_last=5):
    """Average the last `n_last` polls from all polling firms, weighted by the number of participants."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(min(n_last, len(df))):
            results = df[parties].iloc[i]
            num_people = df['Befragte'].iloc[i]#np.nan_to_num(float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', '')))
            # TODO: Polls from different polling firms have different time spacing. Take this into account.
            prediction += results * num_people
    return _prediction_to_dataframe(_normalize_to_hundred(prediction))

weighted_average(data_dict)


# In[11]:

class WeightedAverageModel(Model):
    """Average the last `n_last` polls from all polling firms, weighted by the number of participants."""

    # TODO: Maybe let this inherit from AverageModel to save __init__ function.
    def __init__(self, n_last=5):
        self.n_last = n_last

    def predict(self, data_dict=data_dict):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(min(self.n_last, len(df))):
                results = df[parties].iloc[i]
                num_people = df['Befragte'].iloc[i]#np.nan_to_num(float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', '')))
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results * num_people
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))

WeightedAverageModel().predict(data_dict)


# In[12]:

def latest(data_dict=data_dict):
    """Average the latest polls from all polling firms."""
    return average(data_dict, n_last=1)

latest(data_dict)


# In[13]:

class LatestModel(AverageModel):
    """Average the latest polls from all polling firms."""

    def __init__(self):
        AverageModel.__init__(self, n_last=1)

LatestModel().predict(data_dict)


# In[14]:

def weighted_latest(data_dict=data_dict):
    """Average the latest polls from all polling firms, weighted by the number of participants."""
    return weighted_average(data_dict, n_last=1)

weighted_latest(data_dict)


# In[15]:

class WeightedLatestModel(WeightedAverageModel):
    """Average the latest polls from all polling firms."""

    def __init__(self):
        WeightedAverageModel.__init__(self, n_last=1)

WeightedLatestModel().predict(data_dict)


# In[16]:

def decay(data_dict=data_dict, decay_factor=0.9):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay)."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(len(df)):
            results = df[parties].iloc[i]
            # TODO: Polls from different polling firms have different time spacing. Take this into account.
            prediction += results * decay_factor**(i+1)
    return _prediction_to_dataframe(_normalize_to_hundred(prediction))

decay(data_dict)


# In[17]:

class DecayModel(Model):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay)."""

    def __init__(self, decay_factor=0.9):
        self.decay_factor = decay_factor

    def fit(self):
        # TODO: Fit decay_factor to get best results.
        pass

    def predict(self, data_dict=data_dict):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(len(df)):
                results = df[parties].iloc[i]
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results * self.decay_factor**(i+1)
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))

DecayModel().predict(data_dict)


# In[18]:

def weighted_decay(data_dict=data_dict, decay_factor=0.9):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay) and each poll is weighted by the number of participants."""
    prediction = np.zeros(len(parties))
    for df in data_dict.values():
        for i in range(len(df)):
            results = df[parties].iloc[i]
            num_people = df['Befragte'].iloc[i]#np.nan_to_num(float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', '')))
            # TODO: Polls from different polling firms have different time spacing. Take this into account.
            prediction += results * decay_factor**(i+1) * num_people
    return _prediction_to_dataframe(_normalize_to_hundred(prediction))

weighted_decay(data_dict)


# In[19]:

class WeightedDecayModel(Model):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay) and each poll is weighted by the number of participants."""

    # TODO: Maybe let this inherit from DecayModel to save __init__ function.
    def __init__(self, decay_factor=0.9):
        self.decay_factor = decay_factor

    def fit(self, data_dict=data_dict):
        # TODO: Fit decay_factor to get best results.
        pass

    def predict(self, data_dict=data_dict):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(len(df)):
                results = df[parties].iloc[i]
                num_people = df['Befragte'].iloc[i]#np.nan_to_num(float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', '')))
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results * self.decay_factor**(i+1) * num_people
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))

WeightedDecayModel().predict(data_dict)


# In[ ]:

class LinearRegressionModel(Model):

    def fit(self, data_dict=data_dict):
        pass

    def predict(self, data_dict=data_dict):
        pass


# In[250]:

def apply_model(data_dict=data_dict, model=average, **kwargs):
    """Make a prediction using `model` for each time point in the data."""
    num_timesteps = max([len(df) for df in data_dict.values()])  # take the max from all dataframes
    #print('Applying model to {} time points...'.format(num_timesteps))

    prediction_df = model(data_dict, **kwargs)

    for i in range(1, num_timesteps):
        sliced_data_dict = {key: df[i:] for key, df in data_dict.items()}
        # TODO: Maybe speed up models, especially the decay models.
        # Note: Appending the data frames takes up almost no time here, the bottleneck is the model.
        # TODO: Due to ill-formated data, the resulting dataframe contains NaNs sometimes.
        prediction_df = prediction_df.append(model(sliced_data_dict, **kwargs), ignore_index=True)

    return prediction_df

#pd.options.display.max_rows = 300
#apply_model(data_dict, average)


# In[154]:

def score_predictions(data_dict, prediction_df, polling_firm='allensbach'):
    """Calculate the mean squared error for the predictions in `prediction_df` vs the polling results from `polling_firm`. Average over all parties."""
    # TODO: Have data_dict as parameter here? Or hand over data_dict['allensbach'] directly?
    # TODO: Refactor this once the model is wrapped in a class.
    mse = 0
    for party in parties:
        true_results = data_dict[polling_firm][party]
        predicted_results = prediction_df[party][1:1+len(true_results)]  # first point is prediction for the future, do not use it
        mse += np.mean((true_results - predicted_results)**2)
    return mse / len(parties)


# In[155]:

def score_model(data_dict, model, polling_firm=None, **kwargs):
    """Calculate the mean squared error for the predictions from `model` vs the polling results from `polling_firm`. Average over all parties."""
    # TODO: Refactor this once the model is wrapped in a class.
    prediction_df = apply_model(data_dict, model, **kwargs)

    if polling_firm is None:
        return {polling_firm: score_predictions(data_dict, prediction_df, polling_firm=polling_firm) for polling_firm in data_dict}
    else:
        return score_predictions(data_dict, prediction_df, polling_firm=polling_firm)


#score_model(data_dict, average)
