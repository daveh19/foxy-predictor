import numpy as np
import datetime as dt
import pandas as pd
from scipy.stats.mstats import mquantiles
from  scipy.optimize import curve_fit as fit

import copy as cp

import model_helper

class predict_till_election ():
    '''
    Each model gives 2 outputs: the traces for the parties, and the quantiles at 5%, 50% and 95%.
    **kwargs : "weeks" how many weeks back in the past are used
    
    '''
    
    def __init__ (self, timeline, predict_f = 'montecarlo'):
        
        self.timeline = timeline
        self.funcs_dict = {'montecarlo': self.montecarlo,
                           'linear': self.linear,
                           'quadratic': self.quadratic}
        self.predict_f = self.funcs_dict[predict_f]
        self.election_date = model_helper.election_date #dt.date.strptime('24.09.2017', '%d.%m.%Y')
        self.weeks = model_helper.weeks_left(timeline)
        self.parties  = np.array(model_helper.parties)
        self.result = []
    
    def predict(self, **kwargs):
        self.predict_f(**kwargs)
        self.make_result()
        final_df = pd.concat([self.timeline,self.result])
        final_df = final_df.sort_values('Datum',ascending=False)
        return final_df
        
    def make_result(self):
        
        dates = self.timeline.Datum[0] +np.array([dt.timedelta(weeks=i) for i in range(self.weeks) ])
        
        self.result = pd.DataFrame(columns= self.parties, index= range(self.weeks))
        
        for i,party in enumerate(self.parties):
            for j in range(len(self.quantiles[i].T)):
                
                self.result[party].iloc[j] = self.quantiles[i].T[j]
        
        self.result.insert(0,'Datum',dates)
        self.result.index = -self.result.index
        self.result=  self.result.drop(0,axis=0)


        
    def histograms(self):
        #Returning last timepoint of predictions for all parties
        #Plotting as histogram via:  for i in range(7):
        #plt.hist(test.traces[:,i,-1],bins=np.arange(0,60,.5),normed=True,alpha=.2)
        return self.traces[:,:,-1]
    
    
    
    
    def montecarlo(self, iterations = 100, **kwargs):
        self.help_timeline=  cp.deepcopy(self.timeline[self.parties]).applymap(lambda x: x[1])
        #print ((iterations,self.weeks,len(self.parties)))
        self.traces = np.empty ((iterations,len(self.parties),self.weeks))
        
        covar = self.help_timeline[self.parties].cov()

        for i in range(iterations):
            self.traces[i] =self.n_weeks_predict(covar).T
            #if (100*i/iterations) == int ((100*i/iterations)):
            #    print ("\r %d" %(100*i/iterations), end = '')
        #print("\r 100%")
        self.quantiles = np.array([mquantiles(self.traces[:,i,:], prob = (0.05,0.5,0.95), axis= 0) for i in range(len(self.parties))])

        
        
    def n_weeks_predict (self, covar):
        trace = np.empty((self.weeks,len(self.parties)))
        
        props = self.help_timeline[self.parties].iloc[0]
        trace [0] = props
        
        for i in range (1,self.weeks):
            props+=np.random.multivariate_normal(np.zeros(len(self.parties)) , covar)
            props[props<0]=0
            props= props/(props.sum()) *100
            trace[i] = props
        return trace
    
    def linear (self,iterations= 100,**kwargs):
        
        self.traces = []
        for _ in range(iterations):
            trace = []
            pd.DataFrame.to_xarray
            sample = self.timeline.iloc[0][self.parties].apply(lambda x : np.random.normal(x[1],scale=x[1]-x[0]))
            self.traces.append(sample)
            
        self.traces = np.array(self.traces).reshape(iterations,len(self.parties),1)
        self.quantiles = np.zeros((len(self.parties),3,self.weeks))
        helper = [self.timeline.iloc[0][party] for party in self.parties]
        for i in range(len(self.parties)):
            
            self.quantiles[i] = np.tile(np.array(helper)[i][:],self.weeks).reshape(self.weeks,-1).T
        #self.quantiles = np.tile(self.quantiles,self.weeks).reshape(len(self.parties),3,self.weeks)
        #self.quantiles = np.tile(self.timeline.iloc[0][self.parties].reshape(len(self.parties),3,-1), (1,self.weeks))
        
    def quadratic (self, iterations =100, **kwargs):
        if 'weeks' in kwargs:
            weeks_for_fit = kwargs['weeks']
        else :
            weeks_for_fit = -1
            
        #popts = np.zeros((3, len(self.timeline.iloc[:weeks_for_fit])))
        quad = lambda x,a,b,c : a +x*b+ c*x**2  
        self.traces = []
        for _ in range(iterations):
            trace = []
            sample = self.timeline[self.parties].applymap(lambda x : np.random.normal(x[1],scale=x[1]-x[0]))
            for ind, party in enumerate( self.parties):
                popt, pcovs = fit(quad,np.arange(len(sample.iloc[:weeks_for_fit][party])),sample.iloc[:weeks_for_fit][party])

                trace.append(quad(np.arange(-self.weeks,len(sample[party])),*popt) )

            self.traces.append(trace)
        self.traces = np.array(self.traces)
        #print(self.traces.shape)
        self.quantiles = np.array([mquantiles(self.traces[:,i,:], prob = (0.05,0.5,0.95), axis= 0) \
                                   for i in range(len(self.parties))])[:,:,:self.weeks]