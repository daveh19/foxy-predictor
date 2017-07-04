import sys
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) #current directory
DATA_PATH = DIR_PATH + '/data'# where to save data to/ read data from

PARTIES = ['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AfD', 'Sonstige']

POLLING_FIRMS = ['allensbach', 'emnid', 'forsa', 'politbarometer', 'gms', 'dimap', 'insa']

MODELS = ['----', 'AverageModel', 'WeightedAverageModel', 'LatestModel', 'WeightedLatestModel', 'DecayModel', 'WeightedDecayModel', 'LinearRegressionModel']

HELP_TEXT = 'still no help for you....'
