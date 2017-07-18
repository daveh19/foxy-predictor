# This file contains all model classes

 # TODO: Dirty hack to import from sibling dir. Put wahlrecht_polling_firms.py into the same folder as this file eventually.
import sys
import os
sys.path.append(os.path.abspath('../Backend'))
import scipy as sp
import datetime
import numpy as np
import pandas as pd
from scipy.stats.mstats import mquantiles

from model_helper import _prediction_to_dataframe
from model_helper import _normalize_to_hundred
from model_helper import parties
from model_helper import election_date
from model_helper import weeks_left

#import preprocessing

#import wahlrecht_polling_firms

#data_dict = wahlrecht_polling_firms.get_tables()
#data = preprocessing.average(data_dict, 'simple')
data = None

class Model():



    def fit(self, df=data):
        """Optional fit step to call before predictions. Leave empty if the model does not support fitting."""
        return

    def predicts(self):
        return False
    def predict(self, df=data):
        raise NotImplementedError()

    def predict_all(self, df=data,**kwargs):
        """Make a prediction for each time point in the data."""
        #print('Applying model to {} time points...'.format(len(data)))

        # First prediction, append the other ones below.
        prediction_df = self.predict(df)

        for i in range(1, len(df)):
            # Note: Appending the data frames takes up almost no time here, the bottleneck is the model.
            prediction_df = prediction_df.append(self.predict(df[i:]), ignore_index=True)

        return prediction_df

    # TODO: With the new averaging in preprocessing, scoring the model against different polling firms isn't that simple any more. Maybe make a function in preprocessing that converts the data of a single polling firm to the weekly format.
    def score(self, data=data, polling_firm=None):
        """Calculate a score for the model (lower is better). The score is the mean squared error between the model's predictions and the true results.
        If `polling_firm` is None (default), return a dict with the score for each polling firm. Otherwise, return only the score for that polling firm."""
        prediction_df = self.predict_all(data)
        return mse(data, prediction_df)

        #if polling_firm is None:
        #    return {polling_firm: mse(poll_df, prediction_df) for polling_firm, poll_df in data_dict.items()}
        #else:
        #    return mse(data_dict[polling_firm], prediction_df)


# In[97]:

class PolynomialModel(Model):
    """Fit a polynomial of degree `degree` (from 0 to 3) through the last `n_last` polls and calculate one point into the future."""

    def __init__(self, n_last=5, degree=1):
        self.n_last = n_last
        self.degree = degree

    def predict(self, df=data):
        # TODO: Double-check that this works properly.
        prediction = []
        prediction_error = []

        if self.n_last == None:  # use all rows
            num_rows = len(df)
        else:  # use just the n_last rows
            num_rows = self.n_last

        data_for_regression = df[parties].iloc[:num_rows].fillna(0)
        x_pred = data_for_regression.index.values[0] - 1

        # TODO: Use dropna here.
        # Drop rows that contain only NaN values.
        data_for_regression = data_for_regression[[not (row == 0).all() for _, row in data_for_regression.iterrows()]]

        x = data_for_regression.index.values

        for party in parties:
            y = data_for_regression[party]

            if len(x) > 1 and len(y) > 1:
                #fit_params, fit_cov = np.polyfit(x, y, self.degree, cov=True)
                # Make the fit using scipy.optimize.curve_fit
                f = lambda x, *p: np.polyval(p, x)
                p0 = [1] * (self.degree+1)
                fit_params, fit_cov = sp.optimize.curve_fit(f, x, y, p0)  # TODO: Change f to just take the num of parameters.

                y_pred = np.poly1d(fit_params)(x_pred)
                y_error = np.sqrt(np.diag(np.absolute(fit_cov)))  # these is the uncertainty of the fit for the original data points
                y_error = np.mean(y_error)  # take the mean of all uncertainties to get an estimate of the prediction error
                if np.isinf(y_error):
                    y_error = 0
            else:
                y_pred = np.nan
                y_error = 0

            prediction.append(y_pred)
            prediction_error.append(y_error)

        prediction = _normalize_to_hundred(prediction)

        prediction_df = pd.DataFrame(columns=parties + ['Datum'], index=[0])
        prediction_df['Datum'].iloc[0] = df['Datum'].iloc[0] + datetime.timedelta(weeks=1)
        for i, party in enumerate(parties):
            mean = prediction[i]
            error = prediction_error[i]
            prediction_df[party][0] = [mean - error, mean, mean + error]
        return prediction_df

# In[98]:

class LinearModel(PolynomialModel):
    """Fit a line through the last `n_last` polls and calculate one point into the future."""

    def __init__(self, n_last=5):

        PolynomialModel.__init__(self, n_last=n_last, degree=1)


# In[89]:

class DecayModel(Model):
    """Average the last `n_last` polls (`None`, i.e. all by default), where polls further back are weighted less (exponential decay)."""

    def __init__(self, n_last=None, decay_factor=0.9):
        self.n_last = n_last
        self.decay_factor = decay_factor

    def fit(self):
        # TODO: Fit decay_factor to get best results.
        pass

    # TODO: Maybe generalize by letting AverageModel and DecayModel inherit from each other or common base class.
    def predict(self, df=data):
        prediction = np.zeros(len(parties))
        prediction_error = np.zeros(len(parties))

        if self.n_last == None:  # use all rows
            num_rows = len(df)
        else:  # use just the n_last rows
            num_rows = self.n_last

        # TODO: Take decaying average of uncertainties according to p * (1-p) / n.

        for i in range(min(num_rows, len(df))):  # do not use more rows than the dataframe has
            results = df[parties].iloc[i].fillna(0)
            if not (results == 0).all():  # ignore empty rows
                prediction += results * self.decay_factor**(i+1)

                # Calculate error according to formula from paper: sqrt(p * (1-p) / n)
                p = results / 100
                n = df['Befragte'].fillna(0).iloc[i]
                if n > 0:
                    errors = 100 * np.sqrt(p * (1 - p) / n)
                    prediction_error += errors * self.decay_factor**(i+1)

        prediction = _normalize_to_hundred(prediction)

        prediction_df = pd.DataFrame(index=[0], columns=parties + ['Datum'])
        prediction_df['Datum'].iloc[0] = df['Datum'].iloc[0] + datetime.timedelta(weeks=1)
        for i, party in enumerate(parties):
            mean = prediction[i]
            error = prediction_error[i]
            prediction_df[party][0] = [mean - error, mean, mean + error]

        return prediction_df


# In[90]:

class AverageModel(DecayModel):
    """Average the last `n_last` polls (5 by default)."""

    def __init__(self, n_last=5):
        DecayModel.__init__(self, n_last=n_last, decay_factor=1)

# In[92]:

class LatestModel(AverageModel):
    """Use the latest poll."""

    def __init__(self):
        AverageModel.__init__(self, n_last=1)

# In[105]:

# To install GPFlow:
# pip install tensorflow
# pip install git+https://github.com/GPflow/GPflow
try:
    import GPflow
except ImportError:
    print('GPflow not installed, GPModel cannot be used')

class GPModel(Model):
    """In contrast to the other models, GPModel always makes predictions for all time points. Therefore, `predict` just returns the latest data point from `predict_all`."""


    def __init__(self, variance=2, lengthscales=1.2):

        k = GPflow.kernels.Matern32(1, variance=variance, lengthscales=lengthscales)
        self.kernel=k

    def predicts(self):
        return True

    def predict(self, df=data,**kwargs):
        return self.predict_all(df,**kwargs).iloc[0]

    def histogram(self,samples = 1000):
        return self.traces[:,:,0]

    def predict_all(self, df=data,samples = 1000):
        Y = df[parties]
        Y = Y.dropna(how='all').fillna(0)
        X = Y.index.values

        #X = pd.to_datetime(data.Datum)
        #X=-(X-dt.date.today()).astype('timedelta64[D]').reshape(-1,1)
        X = -X.reshape(-1,1).astype(float)

        #print(Y)

        self.m = GPflow.gpr.GPR(X, pd.DataFrame.as_matrix(Y), kern=self.kernel)
        self.m.optimize()
        weeks2election = weeks_left(df)
        x_pred = np.linspace(+weeks2election+X[0,0],X[-1,0], len(df)+weeks2election).reshape(-1,1)



        trace = self.m.sample(samples, verbose=True, epsilon=0.03, Lmax=15)
        sample_df = self.m.get_samples_df(trace)
        sample_df.head()
        mean, var = self.m.predict_y(x_pred)

        self.traces = np.zeros((samples,len(parties),len(x_pred)))
        count=0
        for i, s in sample_df.iterrows():
            self.m.set_parameter_dict(s)

            f = self.m.predict_f_samples(x_pred, 1)
            self.traces[count] = f[0,:,:].T
            count+=1

        stds = np.sqrt(var)
        # TODO: Integrate this into _normalize_to_hundred.

        prediction = 100 * mean / np.sum(mean, axis=1).reshape(-1, 1)
        prediction_df = pd.DataFrame(index=range(-weeks2election+1,len(df)), columns=parties + ['Datum'])
        #print(prediction_df)
        #print(len(df),len(prediction_df['Datum'][weeks2election-1:] ))
        dates_to_election = election_date -np.array([datetime.timedelta(weeks=i) for i in range(weeks2election-1) ])
        prediction_df['Datum'][:weeks2election-1] = dates_to_election
        prediction_df['Datum'][weeks2election-1:] = pd.to_datetime(df['Datum'])
        prediction_df[parties] = prediction_df[parties].applymap(lambda x : [0,0,0])

        total = np.zeros((len(mean),len(parties),3))
        for i, party in enumerate(parties):
            total[:,i,:] = np.array([prediction[:,i]-2*stds[:,i],prediction[:,i],prediction[:,i]+2*stds[:,i]]).T

        for l,k in enumerate(range(-weeks2election+1,len(df))):
            for i, party in enumerate(parties):
                prediction_df.set_value(k,party,total[l,i,:])

        return prediction_df



class BayesDLM(Model):
    """In contrast to the other models, GPModel always makes predictions for all time points. Therefore, `predict` just returns the latest data point from `predict_all`."""



    def predict(self, df=data):
        return self.predict_all(df).iloc[0]

    def predict_all(self, df, itrs=1000):

        #for this one only go back as far as 2015, to avoid errors, cheap fix..
        df = df.fillna(0)[df.Datum > datetime.datetime(2015,1,1)]

        length = len(df)

        #parties
        #parties_dict
        parties_dict = {}
        for party in parties:
            parties_dict[party] = np.zeros((itrs,length))

        #belief in prior as strong as if it were an average size measurement
        pseudonobs = df['Befragte'].mean()
        i = 0;
        #gammadist
        g = lambda a,b:np.random.gamma(a,b)
        #random number of supporters
        h = lambda l,u:np.random.randint(l,u);

        #average
        avg=np.zeros(7)
        while i < itrs:

            prior = np.zeros(7)
            #prior in first measurement is +-3%
            prior = np.array([h(df[party].iloc[0]*.97,df[party].iloc[0]*1.03) for party in parties])

            sample = np.zeros(7);
            s=np.zeros(7)

            for week_idx,week in enumerate(df.index):
            #    if week == 0:
            #        post = data[week] + prior
            #    else:
                    post = df[parties].loc[week]*df['Befragte'].loc[week]/100 + sample*pseudonobs


                    sample  = np.array([g(post[party] if post[party]>0 else .00001,1) for party in parties])

                    sample = sample/np.sum(sample)
                    for p_idx,party in enumerate(parties):
                        parties_dict[party][i][week_idx] = sample[p_idx]


                    # random-walk
                    s = sample + np.array([g(post[k],1) for k in range(7)])
                    sample = s/(np.sum(s))
                    if week_idx==length-1:
                        avg += post
                        i += 1
                        print( '\r{0:3.2f}% completed'.format(i/itrs*100),end='')
        #print (avg/itrs) # print Dirich params
        prediction_df = pd.DataFrame(index=range(len(df)), columns=parties + ['Datum'])
        prediction_df['Datum'] = df['Datum']
        total = np.zeros((len(df),len(parties),3))
        for p_idx, party in enumerate(parties):
            total[:,p_idx,:] = mquantiles(parties_dict[party],prob=[.025,.5,.975],axis=0).T

        total *=100
        prediction_df[parties] = prediction_df[parties].applymap(lambda x : [0,0,0])
        for k in range(len(df)):
            for p_idx, party in enumerate(parties):
                prediction_df.set_value(k,party,total[k,p_idx,:])

        return prediction_df
