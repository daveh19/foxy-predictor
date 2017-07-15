import sys
import os
import model_classes
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) #current directory
DATA_PATH = DIR_PATH + '/data'# where to save data to/ read data from

PARTIES = ['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AfD', 'Sonstige']

POLLING_FIRMS = ['allensbach', 'emnid', 'forsa', 'politbarometer', 'gms', 'dimap', 'insa', 'public', 'yougov', 'research', 'psephos', 'behrens']

#MODELS = ['----', 'AverageModel', 'WeightedAverageModel', 'LatestModel', 'WeightedLatestModel', 'DecayModel', 'WeightedDecayModel', 'LinearRegressionModel']

MODELS = ['----', 'AverageModel', 'LatestModel', 'PolynomialModel', 'LinearModel', 'DecayModel', 'GPModel']
MODELS_classes = [None, model_classes.AverageModel, model_classes.LatestModel, model_classes.PolynomialModel, model_classes.LinearModel, model_classes.DecayModel, model_classes.GPModel]

HELP_TEXT = 'still no help for you....'
