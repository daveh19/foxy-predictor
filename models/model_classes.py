# This file contains all model classes

 # TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
import wahlrecht_polling_firms

import numpy as np
import pandas as pd
from model_helper import _prediction_to_dataframe
from model_helper import _normalize_to_hundred
from model_helper import parties

class Model():

    def __init__(self):
        self.miao = 'miao'
    
    def fit(self, data_dict=None):
        """Optional fit step to call before predictions. Leave empty if the model does not support fitting."""
        return
    
    def predict(self, data_dict=None):
        raise NotImplementedError()
    
    def predict_all(self, data_dict=None):
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
    
    def score(self, data_dict=None, polling_firm=None):
        """Calculate a score for the model (lower is better). The score is the mean squared error between the model's predictions and the   true results.
        If `polling_firm` is None (default), return a dict with the score for each polling firm. Otherwise, return only the score for that polling firm."""
        prediction_df = self.predict_all(data_dict)
    
        if polling_firm is None:
            return {polling_firm: mse(poll_df, prediction_df) for polling_firm, poll_df in data_dict.items()}
        else: 
            return mse(data_dict[polling_firm], prediction_df)



class AverageModel(Model):
    """Average the last `n_last` polls from all polling firms."""
    
    def __init__(self, n_last=5):
        self.n_last = n_last
        
    def predict(self, data_dict=None):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(min(self.n_last, len(df))):  # do not use more rows than the dataframe has
                results = df[parties].iloc[i]
                # TODO: Polls from different polling firms have different time spacing. Take this into account. 
                prediction += results
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))
        

class WeightedAverageModel(Model):
    """Average the last `n_last` polls from all polling firms, weighted by the number of participants."""

    # TODO: Maybe let this inherit from AverageModel to save __init__ function.
    def __init__(self, n_last=5):
        self.n_last = n_last

    def predict(self, data_dict=None):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(min(self.n_last, len(df))):
                results = df[parties].iloc[i]
                num_people = df['Befragte'].iloc[i]#np.nan_to_num(float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', '')))
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results * num_people
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))


class LatestModel(AverageModel):
    """Average the latest polls from all polling firms."""

    def __init__(self):
        AverageModel.__init__(self, n_last=1)


class WeightedLatestModel(WeightedAverageModel):
    """Average the latest polls from all polling firms."""

    def __init__(self):
        WeightedAverageModel.__init__(self, n_last=1)


class DecayModel(Model):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay)."""

    def __init__(self, decay_factor=0.9):
        self.decay_factor = decay_factor

    def fit(self):
        # TODO: Fit decay_factor to get best results.
        pass

    def predict(self, data_dict=None):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(len(df)):
                results = df[parties].iloc[i]
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results * self.decay_factor**(i+1)
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))


class WeightedDecayModel(Model):
    """Average all polls from all polling firms, where polls further back are weighted less (exponential decay) and each poll is weighted by the number of participants."""

    # TODO: Maybe let this inherit from DecayModel to save __init__ function.
    def __init__(self, decay_factor=0.9):
        self.decay_factor = decay_factor

    def fit(self, data_dict=None):
        # TODO: Fit decay_factor to get best results.
        pass

    def predict(self, data_dict=None):
        prediction = np.zeros(len(parties))
        for df in data_dict.values():
            for i in range(len(df)):
                results = df[parties].iloc[i]
                num_people = df['Befragte'].iloc[i]#np.nan_to_num(float(df['Befragte'].iloc[i].replace('.', '').replace('T • ', '').replace('O • ', '')))
                # TODO: Polls from different polling firms have different time spacing. Take this into account.
                prediction += results * self.decay_factor**(i+1) * num_people
        return _prediction_to_dataframe(_normalize_to_hundred(prediction))



class LinearRegressionModel(Model):

    def fit(self, data_dict=None):
        pass

    def predict(self, data_dict=None):
        pass




