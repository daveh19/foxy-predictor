# TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
import wahlrecht_polling_firms

import numpy as np
import pandas as pd

parties = ['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AfD', 'Sonstige']
election_date = pd.to_datetime('24.09.2017')


def _preprocess_df(df):
    df = df.fillna(0)  # TODO: Some values are NaN --> how to handle these? Especially, the numbers have to add up to 1.
    #df['Befragte'] = df['Befragte'].apply(lambda x: int(x.replace('.', '').replace('NaN', '0')))  # TODO: Befragte column is string so far. Sometimes, there are also NaN values --> how to handle these? Should the polls be ignored for weighting or should an "average" value be used?
    #df[parties] /= 100  # TODO: Have values as 37 or 0.37?
    return df

def _normalize_to_hundred(x):
    """Normalize an array so that its sum is 1."""
    return 100 * x / np.sum(x)

def _prediction_to_dataframe(prediction):
    """Wrap an array with the predictions into a dataframe containing the party names."""
    return pd.DataFrame(data=[prediction], columns=parties)

def weeks_left(timeline):
        most_recent_poll = election_date  - pd.to_datetime (timeline['Datum']) #TODO: make sure it's always "Datum"
        
        #+1 in order to actually include election date
        return int((most_recent_poll).astype('timedelta64[W]')[0])+1


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
